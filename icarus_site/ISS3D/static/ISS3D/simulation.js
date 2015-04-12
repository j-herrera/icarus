var container, stats;
var camera, controls, scene, renderer;
var initialTime = new Date();
var ii = 0;

init();
render();

function init() {
	container = document.createElement('div');
	document.body.appendChild(container);

	//camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.01, 1000 );
	camera = new THREE.OrthographicCamera( window.innerWidth/200 / - 2, window.innerWidth/200 / 2, window.innerHeight/200 / 2, window.innerHeight/200 / - 2, 0.01, 100);
	camera.position.z = 1.5;

	controls = new THREE.OrbitControls( camera );
	controls.damping = 0.2;
	controls.addEventListener( 'change', render );

	scene = new THREE.Scene();
	
	var light	= new THREE.AmbientLight( 0x202020 )
	scene.add( light )
	
	Date.prototype.getJulian = function() {
		return Math.floor((this / 86400000) - (this.getTimezoneOffset()/1440) + 2440587.5);
	}

	var today = new Date();
	var julian = today.getJulian(); 
	
	ml = julian - 2451545.0;
	L = 280.460 + 0.9856474 * ml;
	g = 357.528 + 0.9856003 * ml;
	lambda = L + 1,915 * Math.sin(g*Math.PI/180) + 0.02 * Math.sin(2*g*Math.PI/180);
	beta = 0;
	epsilon = 23.439 - 0.0000004*ml;
	
	alpha = Math.atan(Math.cos(epsilon*Math.PI/180) * Math.tan(lambda*Math.PI/180))
	delta = Math.asin(Math.sin(epsilon*Math.PI/180) * Math.sin(lambda*Math.PI/180))
	
	ST = 360 /(today.getUTCHours()+today.getUTCHours()/60+today.getUTCMinutes()/60) * Math.PI /180;
	
	var light	= new THREE.DirectionalLight( 0x888888, 1 )
	light.position.set(10 *Math.cos(alpha+ST),10*Math.sin(alpha+ST),10*Math.sin(delta))
	scene.add( light )
	

	var PI2 = Math.PI * 2;

	var json, req = new XMLHttpRequest();
	req.open("GET", "api/getJ2TLE", false);
	req.send(null);
	if (req.status == 200) {
		json = req.responseText;
	} else {
		console.log('No Ajax received!');
		json = '[{"inc":0,"raan":0,"ecc":0, "aper":0}]';
	}

	var obj = JSON.parse(json);
	console.log(obj);
	
	n = obj['mm'] * 2 * Math.PI / 3600 /24;
	sma = Math.pow( 398600.4418 / Math.pow(n, 2) , 1/3.0)
	sma = sma/6371/2;
	
	var geometry_iss = new THREE.TorusGeometry( sma, 0.005, 16, 100 );
	var material_iss = new THREE.MeshBasicMaterial( { color: 0xff0000 } );
	var orbit = new THREE.Mesh( geometry_iss, material_iss );
	
	
	var m = new THREE.Matrix4();

	var m1 = new THREE.Matrix4();
	var m2 = new THREE.Matrix4();
	var m3 = new THREE.Matrix4();

	var alpha = 0;
	var beta = Math.PI;
	var gamma = Math.PI/2;

	m1.makeRotationZ( obj['raan']*Math.PI/180);
	m2.makeRotationX( obj['inc']*Math.PI/180 );
	m3.makeRotationZ( obj['aper']*Math.PI/180);

	m.multiplyMatrices( m1, m2 );
	m.multiply( m3 );
	
	orbit.rotateX(Math.PI/2);

	orbit.applyMatrix(m);
	
	scene.add( orbit);	
	
	
	var geometry_earth   = new THREE.SphereGeometry(0.5, 32, 32)
	var material_earth  = new THREE.MeshPhongMaterial()
	
	material_earth.map    = THREE.ImageUtils.loadTexture('/static/ISS3D/2_no_clouds_8k.jpg')
	material_earth.bumpMap    = THREE.ImageUtils.loadTexture('/static/ISS3D/elev_bump_8k.jpg')
	material_earth.bumpScale = 0.05
	material_earth.specularMap    = THREE.ImageUtils.loadTexture('/static/ISS3D/water_8k.png')
	material_earth.specular  = new THREE.Color('grey')

	
	var earthMesh = new THREE.Mesh(geometry_earth, material_earth)
	scene.add(earthMesh)
	
	var clouds =  new THREE.Mesh(
		new THREE.SphereGeometry(0.51, 32, 32),
		new THREE.MeshPhongMaterial({
		map: THREE.ImageUtils.loadTexture('/static/ISS3D/fair_clouds_4k.png'),
		transparent: true
		})
	);
	scene.add(clouds);
	
	
	var geometry_sky  = new THREE.SphereGeometry(5, 32, 32)
	var material_sky  = new THREE.MeshBasicMaterial()
	material_sky.map   = THREE.ImageUtils.loadTexture('/static/ISS3D/sky.jpg')
	material_sky.side  = THREE.BackSide
	var mesh_sky  = new THREE.Mesh(geometry_sky, material_sky)
	scene.add(mesh_sky)
	
	
	
	renderer = new THREE.WebGLRenderer( { antialias: false } );
	renderer.setSize( window.innerWidth, window.innerHeight );
	container.appendChild( renderer.domElement );

	window.addEventListener( 'resize', onWindowResize, false );

	animate();
}

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize( window.innerWidth, window.innerHeight );

	render();
}

function animate() {
	requestAnimationFrame( animate );
	controls.update();
}

function render() {
	renderer.render( scene, camera );
	var today = new Date();
	var julian = today.getJulian(); 
	var localTime = today - initialTime;
	localTime /= 1000.0
	var json, req = new XMLHttpRequest();
	req.open("GET", "api/getJ2TLE", false);
	req.send(null);
	if (req.status == 200) {
		json = req.responseText;
	} else {
		console.log('No Ajax received!');
		json = '[{"inc":0,"raan":0,"ecc":0, "aper":0}]';
	}

	var obj = JSON.parse(json);
	console.log(obj);
	
	n = obj['mm'] * 2 * Math.PI / 3600 /24;
	sma = Math.pow( 398600.4418 / Math.pow(n, 2) , 1/3.0)
	sma = sma/6371/2;
	
	var geometry_iss = new THREE.TorusGeometry( sma, 0.005, 16, 100 );
	var material_iss = new THREE.MeshBasicMaterial( { color: 0xff0000 } );
	var orbit = new THREE.Mesh( geometry_iss, material_iss );
	
	
	var m = new THREE.Matrix4();

	var m1 = new THREE.Matrix4();
	var m2 = new THREE.Matrix4();
	var m3 = new THREE.Matrix4();

	var alpha = 0;
	var beta = Math.PI;
	var gamma = Math.PI/2;

	m1.makeRotationZ( obj['raan']*Math.PI/180 + 10 *obj['dRaanByDt'] * localTime);
	m2.makeRotationX( obj['inc']*Math.PI/180 );
	m3.makeRotationZ( obj['aper']*Math.PI/180  + 10 *obj['dAperByDt'] * localTime);

	m.multiplyMatrices( m1, m2 );
	m.multiply( m3 );
	
	orbit.rotateX(Math.PI/2);

	orbit.applyMatrix(m);
	
	scene.add( orbit);
}
