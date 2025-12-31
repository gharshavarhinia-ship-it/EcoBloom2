// Global variables
let allPlants = [];
let currentPage = 'home';

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadPlants();
    checkWateringReminders();
    // Check reminders every 5 minutes
    setInterval(checkWateringReminders, 300000);
});

// Load all plants from backend
async function loadPlants() {
    try {
        const response = await fetch('/get_plants');
        allPlants = await response.json();
        displayPlants();
        displayGarden();
    } catch (error) {
        console.error('Error loading plants:', error);
        showNotification('Error loading plants. Please refresh the page.');
    }
}

// Display plants on home page
function displayPlants() {
    const grid = document.getElementById('plants-grid');
    grid.innerHTML = '';

    allPlants.forEach(plant => {
        const card = createPlantCard(plant);
        grid.appendChild(card);
    });
}

// Create plant card element
function createPlantCard(plant) {
    const card = document.createElement('div');
    card.className = 'plant-card';
    card.onclick = () => showPlantDetails(plant);

    card.innerHTML = `
        ${plant.saved ? '<div class="saved-badge">✓</div>' : ''}
        <img src="${plant.image || 'https://via.placeholder.com/400x300?text=' + encodeURIComponent(plant.name)}" 
             alt="${plant.name}" 
             class="plant-card-image"
             onerror="this.src='https://via.placeholder.com/400x300?text=${encodeURIComponent(plant.name)}'">
        <div class="plant-card-body">
            <h3 class="plant-card-name">${plant.name}</h3>
            <p class="plant-card-scientific">${plant.scientific_name}</p>
            <span class="plant-card-badge">${plant.sunlight} Sunlight</span>
        </div>
    `;

    return card;
}

// Show plant details in modal
function showPlantDetails(plant) {
    const modal = document.getElementById('plant-modal');
    const modalBody = document.getElementById('modal-body');

    const wateringTimes = plant.watering_times.join(' & ');

    modalBody.innerHTML = `
        <img src="${plant.image || 'https://via.placeholder.com/600x300?text=' + encodeURIComponent(plant.name)}" 
             alt="${plant.name}" 
             class="modal-plant-image"
             onerror="this.src='https://via.placeholder.com/600x300?text=${encodeURIComponent(plant.name)}'">
        <h2 class="modal-plant-name">${plant.name}</h2>
        <p class="modal-scientific-name">${plant.scientific_name}</p>

        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">💧 Watering</div>
                <div class="info-value">${plant.watering_frequency}</div>
            </div>
            <div class="info-item">
                <div class="info-label">⏰ Best Times</div>
                <div class="info-value">${wateringTimes}</div>
            </div>
            <div class="info-item">
                <div class="info-label">☀️ Sunlight</div>
                <div class="info-value">${plant.sunlight}</div>
            </div>
            <div class="info-item">
                <div class="info-label">🌱 Growth Type</div>
                <div class="info-value">${plant.growth_type}</div>
            </div>
        </div>

        <div class="detail-section">
            <h3>🌿 Soil Requirements</h3>
            <p>${plant.soil}</p>
        </div>

        <div class="detail-section">
            <h3>🧪 Fertilizer</h3>
            <p>${plant.fertilizer}</p>
        </div>

        <div class="detail-section">
            <h3>💚 Care & Maintenance Tips</h3>
            <p>${plant.care_tips}</p>
        </div>

        <button class="btn-primary" onclick="toggleSaveToGarden(${plant.id})" id="save-btn-${plant.id}">
            ${plant.saved ? '✓ Saved to Garden' : '+ Save to My Garden'}
        </button>
    `;

    modal.classList.add('active');
}

// Close modal
function closeModal() {
    const modal = document.getElementById('plant-modal');
    modal.classList.remove('active');
}

// Toggle save to garden
async function toggleSaveToGarden(plantId) {
    const plant = allPlants.find(p => p.id === plantId);

    try {
        const endpoint = plant.saved ? `/remove_from_garden/${plantId}` : `/save_to_garden/${plantId}`;
        const response = await fetch(endpoint, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            plant.saved = !plant.saved;
            if (!plant.saved) {
                plant.watering_status = { morning: false, evening: false };
            }

            const btn = document.getElementById(`save-btn-${plantId}`);
            if (btn) {
                btn.textContent = plant.saved ? '✓ Saved to Garden' : '+ Save to My Garden';
            }

            showNotification(data.message);
            displayPlants();
            displayGarden();
        }
    } catch (error) {
        console.error('Error saving plant:', error);
        showNotification('Error saving plant. Please try again.');
    }
}

// Display garden page
function displayGarden() {
    const grid = document.getElementById('garden-grid');
    const noPlants = document.getElementById('no-plants-message');

    const savedPlants = allPlants.filter(p => p.saved);

    if (savedPlants.length === 0) {
        grid.style.display = 'none';
        noPlants.style.display = 'block';
        return;
    }

    grid.style.display = 'grid';
    noPlants.style.display = 'none';
    grid.innerHTML = '';

    savedPlants.forEach(plant => {
        const card = createGardenCard(plant);
        grid.appendChild(card);
    });
}

// Create garden card with watering buttons
function createGardenCard(plant) {
    const card = document.createElement('div');
    card.className = 'garden-card';

    const hasMorning = plant.watering_times.includes('Morning');
    const hasEvening = plant.watering_times.includes('Evening');

    card.innerHTML = `
        <div class="garden-card-header">
            <img src="${plant.image || 'https://via.placeholder.com/80?text=' + encodeURIComponent(plant.name)}" 
                 alt="${plant.name}" 
                 class="garden-card-image"
                 onerror="this.src='https://via.placeholder.com/80?text=${encodeURIComponent(plant.name)}'">
            <div class="garden-card-info">
                <h3>${plant.name}</h3>
                <p>${plant.watering_frequency}</p>
            </div>
        </div>

        <div class="watering-section">
            <h4>🌊 Today's Watering Schedule</h4>
            <div class="watering-buttons">
                ${hasMorning ? `
                    <button class="watering-btn ${plant.watering_status.morning ? 'completed' : ''}" 
                            onclick="markWatering(${plant.id}, 'morning')"
                            ${plant.watering_status.morning ? 'disabled' : ''}>
                        ${plant.watering_status.morning ? '✅' : '🌅'} Morning
                    </button>
                ` : ''}
                ${hasEvening ? `
                    <button class="watering-btn ${plant.watering_status.evening ? 'completed' : ''}" 
                            onclick="markWatering(${plant.id}, 'evening')"
                            ${plant.watering_status.evening ? 'disabled' : ''}>
                        ${plant.watering_status.evening ? '✅' : '🌙'} Evening
                    </button>
                ` : ''}
            </div>
        </div>

        <button class="remove-btn" onclick="toggleSaveToGarden(${plant.id})">
            Remove from Garden
        </button>
    `;

    return card;
}

// Mark watering as done
async function markWatering(plantId, timeOfDay) {
    try {
        const response = await fetch(`/update_watering/${plantId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ time_of_day: timeOfDay })
        });

        const data = await response.json();

        if (data.success) {
            const plant = allPlants.find(p => p.id === plantId);
            plant.watering_status[timeOfDay] = true;
            displayGarden();
            showNotification(`✅ ${timeOfDay.charAt(0).toUpperCase() + timeOfDay.slice(1)} watering completed for ${plant.name}!`);
        }
    } catch (error) {
        console.error('Error updating watering:', error);
        showNotification('Error updating watering status. Please try again.');
    }
}

// Check and show watering reminders
function checkWateringReminders() {
    const savedPlants = allPlants.filter(p => p.saved);
    const currentHour = new Date().getHours();

    savedPlants.forEach(plant => {
        // Morning reminder (6 AM - 10 AM)
        if (currentHour >= 6 && currentHour < 10 &&
            plant.watering_times.includes('Morning') &&
            !plant.watering_status.morning) {
            setTimeout(() => {
                showWateringAlert(plant, 'morning');
            }, Math.random() * 5000); // Random delay to avoid all at once
        }

        // Evening reminder (5 PM - 8 PM)
        if (currentHour >= 17 && currentHour < 20 &&
            plant.watering_times.includes('Evening') &&
            !plant.watering_status.evening) {
            setTimeout(() => {
                showWateringAlert(plant, 'evening');
            }, Math.random() * 5000);
        }
    });
}

// Show watering alert
function showWateringAlert(plant, timeOfDay) {
    const message = `🌱 Don't forget to water your ${plant.name} this ${timeOfDay}!`;

    if (confirm(message + '\n\nMark as watered now?')) {
        markWatering(plant.id, timeOfDay);
    }
}

// Filter plants by search
function filterPlants() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const grid = document.getElementById('plants-grid');

    grid.innerHTML = '';

    const filtered = allPlants.filter(plant =>
        plant.name.toLowerCase().includes(searchTerm) ||
        plant.scientific_name.toLowerCase().includes(searchTerm)
    );

    filtered.forEach(plant => {
        const card = createPlantCard(plant);
        grid.appendChild(card);
    });
}

// Show page
function showPage(pageName) {
    // Update active page
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(`${pageName}-page`).classList.add('active');

    // Update active nav button
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.nav-btn').classList.add('active');

    currentPage = pageName;
}

// Handle photo upload
function handlePhotoUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    // For demo purposes, show a message
    // In a real app, you would use image recognition API
    const plantName = prompt('Could not automatically identify plant. Please enter the plant name:');

    if (plantName) {
        const existingPlant = allPlants.find(p =>
            p.name.toLowerCase() === plantName.toLowerCase()
        );

        if (existingPlant) {
            showPlantDetails(existingPlant);
        } else {
            alert('Plant not found in database. Please add it manually.');
            showAddPlantModal();
        }
    }

    // Reset file input
    event.target.value = '';
}

// Show add plant modal
function showAddPlantModal() {
    const modal = document.getElementById('add-plant-modal');
    modal.classList.add('active');
}

// Close add plant modal
function closeAddPlantModal() {
    const modal = document.getElementById('add-plant-modal');
    modal.classList.remove('active');
    document.getElementById('add-plant-form').reset();
}

// Submit new plant
async function submitNewPlant(event) {
    event.preventDefault();

    const wateringTimes = Array.from(document.querySelectorAll('.watering-time-checkbox:checked'))
        .map(cb => cb.value);

    if (wateringTimes.length === 0) {
        alert('Please select at least one watering time.');
        return;
    }

    const newPlant = {
        name: document.getElementById('new-plant-name').value,
        scientific_name: document.getElementById('new-scientific-name').value,
        image: document.getElementById('new-image-url').value,
        watering_frequency: document.getElementById('new-watering-freq').value,
        watering_times: wateringTimes,
        sunlight: document.getElementById('new-sunlight').value,
        soil: document.getElementById('new-soil').value,
        fertilizer: document.getElementById('new-fertilizer').value,
        growth_type: document.getElementById('new-growth-type').value,
        care_tips: document.getElementById('new-care-tips').value,
        saved: false
    };

    try {
        const response = await fetch('/add_plant', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newPlant)
        });

        const data = await response.json();

        if (data.success) {
            allPlants.push(data.plant);
            displayPlants();
            closeAddPlantModal();
            showNotification('✅ Plant added successfully!');
        }
    } catch (error) {
        console.error('Error adding plant:', error);
        showNotification('Error adding plant. Please try again.');
    }
}

// Show notification
function showNotification(message) {
    const notification = document.getElementById('notification');
    const text = document.getElementById('notification-text');

    text.textContent = message;
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Close modal on outside click
window.onclick = function (event) {
    const plantModal = document.getElementById('plant-modal');
    const addModal = document.getElementById('add-plant-modal');

    if (event.target === plantModal) {
        closeModal();
    }
    if (event.target === addModal) {
        closeAddPlantModal();
    }
}