var container, stats;
var camera, controls, scene, renderer;

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
	
	var light	= new THREE.AmbientLight( 0x888888 )
	scene.add( light )
	
	var light	= new THREE.DirectionalLight( 0xcccccc, 1 )
	light.position.set(5,3,5)
	scene.add( light )


	var PI2 = Math.PI * 2;

	var json, req = new XMLHttpRequest();
	req.open("GET", "api/getTLE", false);
	req.send(null);
	if (req.status == 200) {
		json = req.responseText;
	} else {
		console.log('No Ajax received!');
		json = '[{"inc":0,"raan":0,"ecc":0, "aper":0}]';
	}

	var obj = JSON.parse(json);
	
	n = obj['mm'] * 2 * Math.PI / 3600 /24;
	sma = Math.pow( 398600.4418 / Math.pow(n, 2) , 1/3.0)
	sma = sma/6371/2;
	console.log(sma);
	var geometry_iss = new THREE.TorusGeometry( sma, 0.01, 16, 100 );
	var material_iss = new THREE.MeshBasicMaterial( { color: 0xff0000 } );
	var orbit = new THREE.Mesh( geometry_iss, material_iss );
	
	
	var m = new THREE.Matrix4();

	var m1 = new THREE.Matrix4();
	var m2 = new THREE.Matrix4();
	var m3 = new THREE.Matrix4();

	var alpha = 0;
	var beta = Math.PI;
	var gamma = Math.PI/2;

	m1.makeRotationZ( obj['raan']*Math.PI/180 );
	m2.makeRotationX( obj['inc']*Math.PI/180 );
	m3.makeRotationZ( obj['aper']*Math.PI/180 );

	m.multiplyMatrices( m1, m2 );
	m.multiply( m3 );
	
	orbit.rotateX(Math.PI/2);

	orbit.applyMatrix(m);
	
	scene.add( orbit);
	
	
	
	var geometry_earth   = new THREE.SphereGeometry(0.5, 32, 32)
	var material_earth  = new THREE.MeshPhongMaterial()
	material_earth.map    = THREE.ImageUtils.loadTexture('/static/ISS3D/earthmap1k.jpg')
	var earthMesh = new THREE.Mesh(geometry_earth, material_earth)
	scene.add(earthMesh)
	
	
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
}
