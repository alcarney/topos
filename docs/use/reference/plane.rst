Plane
=====

.. raw:: html

    <script>
        // Based on code found here:
        // https://manu.ninja/webgl-3d-model-viewer-using-three-js/
        let canvas;
        let camera, controls, scene, renderer;
        let lighting, ambient, keyLight, fillLight, backLight;
        let windowHalfX = window.innerWidth / 2;
        let windowHalfY = window.innerHeight / 2;

        // Setup three.js
        function init() {
            // Grab the element where we will place the preview
            canvas = document.getElementById("model-preview");

            // Setup a camera
            camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
            camera.position.x = 2;
            camera.position.y = 2;
            camera.position.z = 3;


            // A Scene and some basic lighting
            scene = new THREE.Scene();
            ambient = new THREE.AmbientLight(0xffffff, 1.0);
            scene.add(ambient);

            // Now to load the materials file
            let mtlLoader = new THREE.MTLLoader();
            mtlLoader.setBaseUrl("/_static/obj/");
            mtlLoader.setPath("/_static/obj/");
            mtlLoader.load('materials.mtl', function(materials) {

                materials.preload();

                let objLoader = new THREE.OBJLoader();
                objLoader.setMaterials(materials);
                objLoader.setPath("/_static/obj/");
                objLoader.load("plane.obj", function(obj) {
                    scene.add(obj);
                });

            });

            // Set up the Renderer
            renderer = new THREE.WebGLRenderer({canvas: canvas});
            canvas.width = canvas.clientWidth;
            canvas.height = canvas.clientHeight;
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setClearColor(new THREE.Color("hsl(0, 0%, 10%)"));
            renderer.setViewport(0, 0, canvas.clientWidth, canvas.clientHeight);

            // Setup the viewport controls
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.25;
            controls.enableZoom = false;

        }

        // The function called each frame to draw
        function render() {
            requestAnimationFrame(render);
            controls.update();
            renderer.render(scene, camera);
        }

        // Only run our code once everything has loaded
        window.onload = function () {
            if (!Detector.webgl) {
                Detector.addGetWebGLMessage();
            }

            init();
            render();
        };
    </script>
    <canvas id="model-preview"></canvas>
