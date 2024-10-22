<template>
  <OAMain title="3D model">
    <div class="app-container">
      <div id="container"></div>
      <div v-if="selectedInfo" class="info-box">
        <h3>Cuboid Info</h3>
        <p><strong>Layer:</strong> {{ selectedInfo.layer }}</p>
        <p><strong>Row:</strong> {{ selectedInfo.row }}</p>
        <p><strong>Column:</strong> {{ selectedInfo.column }}</p>
      </div>
    </div>
  </OAMain>
</template>

<script setup name="3Dmodel">
import OAMain from "@/components/OAMain.vue";
import { ref, onMounted } from "vue";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

const mouse = new THREE.Vector2(); // Mouse position
const selectedInfo = ref(null); // Ref for storing selected cuboid information
let currentSelectedCuboid = null; // Variable to store the currently selected cuboid

onMounted(() => {
  // Create the scene, camera, and renderer
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xffffff); // Set scene background to white
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  const renderer = new THREE.WebGLRenderer({ antialias: true });

  // Set renderer size and append to container
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.getElementById("container").appendChild(renderer.domElement);

  // Enable OrbitControls for camera rotation and zoom
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; // Enable smooth movement
  controls.dampingFactor = 0.1; // Control the damping factor
  controls.screenSpacePanning = false; // Prevent panning into the screen
  controls.maxPolarAngle = Math.PI / 2; // Limit vertical rotation
  controls.minDistance = 10; // Prevent zooming in too close
  controls.maxDistance = 100; // Prevent zooming out too far

  // Set the target of OrbitControls to the center of the scene (0, 0, 0)
  controls.target.set(0, 0, 0);

  // Lighting setup
  const ambientLight = new THREE.AmbientLight(0x404040, 0.5); // Softer ambient light
  scene.add(ambientLight);

  const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight1.position.set(10, 20, 10);
  scene.add(directionalLight1);

  const directionalLight2 = new THREE.DirectionalLight(0xff0000, 0.5);
  directionalLight2.position.set(-10, -20, -10);
  scene.add(directionalLight2);

  // Define cuboid dimensions and intervals
  const cuboidWidth = 6.7;
  const cuboidHeight = 0.5;
  const cuboidDepth = 6.7;
  const cuboidInterval = 0.1;
  const layerInterval = 2.0;

  // Store cuboids in an array for easy access
  const cuboids = [];

  // Function to create a wireframe cuboid
  const createWireframeCuboid = (x, y, z, layer, row, column) => {
    const geometry = new THREE.BoxGeometry(
      cuboidWidth,
      cuboidHeight,
      cuboidDepth
    );
    const wireframe = new THREE.WireframeGeometry(geometry);
    const material = new THREE.LineBasicMaterial({ color: 0x0000ff }); // Change to blue wireframe color
    const line = new THREE.LineSegments(wireframe, material);
    line.position.set(x, y, z);
    line.userData = { layer, row, column }; // Store additional information in userData
    cuboids.push(line); // Add cuboid to the array
    return line;
  };

  // Generate the grid of cuboids
  const numberOfRows = 7;
  const numberOfColumns = 3;
  const numberOfLayers = 3;

  // Calculate starting position for the cuboids
  const startX =
    -(cuboidWidth * numberOfRows + cuboidInterval * (numberOfRows - 1)) / 2;
  const startZ =
    -(cuboidDepth * numberOfColumns + cuboidInterval * (numberOfColumns - 1)) /
    2;

  // Nested loops to create a 3D grid of cuboids
  for (let layer = 0; layer < numberOfLayers; layer++) {
    for (let row = 0; row < numberOfRows; row++) {
      for (let column = 0; column < numberOfColumns; column++) {
        const x = startX + row * (cuboidWidth + cuboidInterval);
        const z = startZ + column * (cuboidDepth + cuboidInterval);
        const y = layer * (cuboidHeight + layerInterval);
        const cuboid = createWireframeCuboid(x, y, z, layer, row, column);
        scene.add(cuboid);
      }
    }
  }

  // Set initial camera position
  camera.position.set(20, 20, 30);
  camera.lookAt(0, 0, 0); // Look at the origin

  // Animation loop to render the scene
  const animate = () => {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  };
  animate();

  // Mouse move event listener for selection
  const raycaster = new THREE.Raycaster(); // Raycaster for mouse selection
  const onMouseMove = (event) => {
    // Update mouse variable with normalized device coordinates
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // Update the raycaster with the camera and mouse position
    raycaster.setFromCamera(mouse, camera);

    // Calculate objects intersecting the raycaster
    const intersects = raycaster.intersectObjects(cuboids);

    // If an intersection occurs
    if (intersects.length > 0) {
      const selectedCuboid = intersects[0].object;

      // If it's a new selection
      if (currentSelectedCuboid !== selectedCuboid) {
        // Reset the previous selected cuboid back to wireframe
        if (currentSelectedCuboid) {
          const previousGeometry = new THREE.BoxGeometry(
            cuboidWidth,
            cuboidHeight,
            cuboidDepth
          );
          const previousMaterial = new THREE.LineBasicMaterial({
            color: 0x0000ff,
          }); // Change to blue wireframe color
          const wireframeCuboid = new THREE.LineSegments(
            new THREE.WireframeGeometry(previousGeometry),
            previousMaterial
          );
          wireframeCuboid.position.copy(currentSelectedCuboid.position);
          scene.remove(currentSelectedCuboid);
          scene.add(wireframeCuboid);
          cuboids.push(wireframeCuboid); // Re-add the wireframe to the array
        }

        // Convert the selected cuboid to a solid mesh
        const selectedGeometry = new THREE.BoxGeometry(
          cuboidWidth,
          cuboidHeight,
          cuboidDepth
        );
        const selectedMaterial = new THREE.MeshStandardMaterial({
          color: 0x0000ff,
        }); // Change to blue solid color
        const solidCuboid = new THREE.Mesh(selectedGeometry, selectedMaterial);
        solidCuboid.position.copy(selectedCuboid.position);
        solidCuboid.userData = selectedCuboid.userData; // Preserve user data
        scene.remove(selectedCuboid); // Remove the wireframe
        scene.add(solidCuboid); // Add the solid cuboid

        // Update selected info
        const { layer, row, column } = solidCuboid.userData; // Get layer, row, column from userData
        selectedInfo.value = { layer, row, column }; // Update selected info

        // Update the current selected cuboid
        currentSelectedCuboid = solidCuboid;
      }
    } else {
      // If no intersection, reset selected info
      if (currentSelectedCuboid) {
        // Convert the selected cuboid back to wireframe
        const previousGeometry = new THREE.BoxGeometry(
          cuboidWidth,
          cuboidHeight,
          cuboidDepth
        );
        const previousMaterial = new THREE.LineBasicMaterial({
          color: 0x0000ff,
        }); // Change to blue wireframe color
        const wireframeCuboid = new THREE.LineSegments(
          new THREE.WireframeGeometry(previousGeometry),
          previousMaterial
        );
        wireframeCuboid.position.copy(currentSelectedCuboid.position);
        scene.remove(currentSelectedCuboid);
        scene.add(wireframeCuboid);
        cuboids.push(wireframeCuboid); // Re-add the wireframe to the array
        currentSelectedCuboid = null; // Reset current selected cuboid
      }
      selectedInfo.value = null; // Reset selected info if no intersection
    }
  };

  window.addEventListener("mousemove", onMouseMove, false);

  // Make the renderer responsive to window resizing
  window.addEventListener("resize", () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
  });
});
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  background-color: white; /* Set app background color to white */
  color: black; /* Black text for better readability */
}

#container {
  flex: 1; /* Allow the container to grow and fill remaining space */
}

.info-box {
  position: absolute;
  top: 12%;
  left: 12%;
  background-color: white; /* Info box background */
  padding: 15px; /* More padding for a better appearance */
  border-radius: 5px;
  color: black; /* Ensure text is black for readability */
  z-index: 10;
  box-shadow: 0 2px 10px rgba(200, 161, 161, 0.5);
}
</style>
