from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

PLANTS_FILE = 'plants.json'

def initialize_plants_data():
    """Initialize plants.json with default data if it doesn't exist"""
    if not os.path.exists(PLANTS_FILE):
        default_plants = [
            {
                "id": 1,
                "name": "Aloe Vera",
                "scientific_name": "Aloe barbadensis miller",
                "image": "https://images.unsplash.com/photo-1596548438137-d51ea5c83065?w=400",
                "watering_frequency": "Once every 2-3 weeks",
                "watering_times": ["Morning"],
                "sunlight": "Partial",
                "soil": "Well-draining cactus/succulent mix",
                "fertilizer": "Diluted liquid fertilizer once in spring",
                "growth_type": "Pot",
                "care_tips": "Allow soil to dry completely between waterings. Great for beginners and has medicinal properties.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 2,
                "name": "Tulsi (Holy Basil)",
                "scientific_name": "Ocimum sanctum",
                "image": "https://images.unsplash.com/photo-1594608661623-aa0bd3a69d98?w=400",
                "watering_frequency": "Daily during summer, alternate days in winter",
                "watering_times": ["Morning", "Evening"],
                "sunlight": "Full",
                "soil": "Rich, loamy soil with good drainage",
                "fertilizer": "Organic compost monthly",
                "growth_type": "Pot or Open Space",
                "care_tips": "Pinch flowers to promote leaf growth. Sacred plant with medicinal benefits. Prefers warm climate.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 3,
                "name": "Rose",
                "scientific_name": "Rosa spp.",
                "image": "https://images.unsplash.com/photo-1518621736915-f3b1c41bfd00?w=400",
                "watering_frequency": "Daily in summer, 3-4 times weekly in winter",
                "watering_times": ["Morning"],
                "sunlight": "Full",
                "soil": "Well-drained, slightly acidic soil rich in organic matter",
                "fertilizer": "Balanced NPK fertilizer every 2-3 weeks during growing season",
                "growth_type": "Open Space or Large Pot",
                "care_tips": "Prune regularly to encourage blooming. Remove dead flowers. Watch for aphids and black spot.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 4,
                "name": "Money Plant",
                "scientific_name": "Epipremnum aureum",
                "image": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400",
                "watering_frequency": "Once or twice weekly",
                "watering_times": ["Morning"],
                "sunlight": "Partial to Shade",
                "soil": "Well-draining potting mix",
                "fertilizer": "Liquid fertilizer once a month",
                "growth_type": "Pot",
                "care_tips": "Excellent air purifier. Can grow in water or soil. Very low maintenance and tolerates neglect.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 5,
                "name": "Cactus",
                "scientific_name": "Cactaceae family",
                "image": "https://images.unsplash.com/photo-1509937528035-ad76254b0356?w=400",
                "watering_frequency": "Once every 2-4 weeks",
                "watering_times": ["Morning"],
                "sunlight": "Full",
                "soil": "Sandy, well-draining cactus mix",
                "fertilizer": "Cactus fertilizer during growing season",
                "growth_type": "Pot",
                "care_tips": "Overwatering is the main cause of death. Needs minimal care. Perfect for dry climates.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 6,
                "name": "Snake Plant",
                "scientific_name": "Sansevieria trifasciata",
                "image": "https://images.unsplash.com/photo-1593482892290-f54927ae1bb4?w=400",
                "watering_frequency": "Once every 2-3 weeks",
                "watering_times": ["Morning"],
                "sunlight": "Partial to Full",
                "soil": "Well-draining cactus or succulent mix",
                "fertilizer": "Diluted all-purpose fertilizer in growing season",
                "growth_type": "Pot",
                "care_tips": "Converts CO2 to oxygen at night. Extremely hardy and drought-tolerant. Avoid overwatering.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 7,
                "name": "Bamboo",
                "scientific_name": "Bambusoideae subfamily",
                "image": "https://images.unsplash.com/photo-1571847352936-e025e4b52b91?w=400",
                "watering_frequency": "Keep soil consistently moist",
                "watering_times": ["Morning", "Evening"],
                "sunlight": "Partial",
                "soil": "Rich, well-draining soil",
                "fertilizer": "Balanced fertilizer monthly during growing season",
                "growth_type": "Open Space or Large Pot",
                "care_tips": "Fast-growing and sustainable. Lucky bamboo can grow in water. Needs humidity and regular watering.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 8,
                "name": "Marigold",
                "scientific_name": "Tagetes spp.",
                "image": "https://images.unsplash.com/photo-1592150621744-aca64f48394a?w=400",
                "watering_frequency": "Daily during hot weather",
                "watering_times": ["Morning"],
                "sunlight": "Full",
                "soil": "Well-drained, moderately fertile soil",
                "fertilizer": "Low-nitrogen fertilizer every few weeks",
                "growth_type": "Pot or Open Space",
                "care_tips": "Deadhead regularly for continuous blooming. Natural pest repellent. Great companion plant for vegetables.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 9,
                "name": "Hibiscus",
                "scientific_name": "Hibiscus rosa-sinensis",
                "image": "https://images.unsplash.com/photo-1615092296061-e2ccfeb2f3d6?w=400",
                "watering_frequency": "Daily in summer, alternate days in winter",
                "watering_times": ["Morning", "Evening"],
                "sunlight": "Full",
                "soil": "Rich, well-draining soil with organic matter",
                "fertilizer": "High-potassium fertilizer weekly during blooming",
                "growth_type": "Open Space or Large Pot",
                "care_tips": "Needs consistent moisture. Prune after flowering. Flowers last only one day but plant blooms continuously.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 10,
                "name": "Peace Lily",
                "scientific_name": "Spathiphyllum spp.",
                "image": "https://images.unsplash.com/photo-1593482892290-f54927ae1bb4?w=400",
                "watering_frequency": "Once or twice weekly",
                "watering_times": ["Morning"],
                "sunlight": "Shade to Partial",
                "soil": "Well-draining potting mix rich in organic matter",
                "fertilizer": "Balanced liquid fertilizer monthly",
                "growth_type": "Pot",
                "care_tips": "Excellent air purifier. Drooping leaves indicate need for water. Mist leaves for humidity. Toxic to pets.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 11,
                "name": "Spider Plant",
                "scientific_name": "Chlorophytum comosum",
                "image": "https://images.unsplash.com/photo-1572688484259-e3d3b8f0d4e3?w=400",
                "watering_frequency": "Twice weekly",
                "watering_times": ["Morning"],
                "sunlight": "Partial",
                "soil": "Well-draining potting mix",
                "fertilizer": "Liquid fertilizer bi-weekly in growing season",
                "growth_type": "Pot",
                "care_tips": "Great air purifier. Produces baby plants on runners. Very easy to propagate and maintain.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 12,
                "name": "Jade Plant",
                "scientific_name": "Crassula ovata",
                "image": "https://images.unsplash.com/photo-1459156212016-c812468e2115?w=400",
                "watering_frequency": "Once every 1-2 weeks",
                "watering_times": ["Morning"],
                "sunlight": "Full to Partial",
                "soil": "Well-draining succulent mix",
                "fertilizer": "Diluted succulent fertilizer quarterly",
                "growth_type": "Pot",
                "care_tips": "Symbol of good luck and prosperity. Avoid overwatering. Can live for decades with proper care.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 13,
                "name": "Areca Palm",
                "scientific_name": "Dypsis lutescens",
                "image": "https://images.unsplash.com/photo-1581689040271-a02129c8ddcc?w=400",
                "watering_frequency": "2-3 times weekly",
                "watering_times": ["Morning"],
                "sunlight": "Partial to Full",
                "soil": "Well-draining, slightly acidic potting mix",
                "fertilizer": "Slow-release palm fertilizer quarterly",
                "growth_type": "Pot or Open Space",
                "care_tips": "Natural air humidifier. Keep soil moist but not waterlogged. Mist leaves regularly. Remove brown fronds.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 14,
                "name": "Mint",
                "scientific_name": "Mentha spp.",
                "image": "https://images.unsplash.com/photo-1628556270448-4d4e4148e1b1?w=400",
                "watering_frequency": "Daily during hot weather",
                "watering_times": ["Morning", "Evening"],
                "sunlight": "Partial",
                "soil": "Rich, moist, well-draining soil",
                "fertilizer": "Compost or balanced fertilizer monthly",
                "growth_type": "Pot",
                "care_tips": "Spreads aggressively - best in containers. Pinch regularly for bushier growth. Great for teas and cooking.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 15,
                "name": "Curry Leaf Plant",
                "scientific_name": "Murraya koenigii",
                "image": "https://images.unsplash.com/photo-1583909312022-c0c6c05b3b6d?w=400",
                "watering_frequency": "Daily in summer, alternate days in winter",
                "watering_times": ["Morning"],
                "sunlight": "Full to Partial",
                "soil": "Well-draining, fertile soil",
                "fertilizer": "Organic compost monthly",
                "growth_type": "Pot or Open Space",
                "care_tips": "Essential in Indian cooking. Aromatic leaves. Prune regularly to encourage bushier growth.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 16,
                "name": "Lavender",
                "scientific_name": "Lavandula spp.",
                "image": "https://images.unsplash.com/photo-1563241714-f99ae5df44c4?w=400",
                "watering_frequency": "Once or twice weekly",
                "watering_times": ["Morning"],
                "sunlight": "Full",
                "soil": "Well-draining, slightly alkaline soil",
                "fertilizer": "Light feeding once or twice per year",
                "growth_type": "Open Space or Large Pot",
                "care_tips": "Drought-tolerant once established. Prune after flowering. Aromatic with calming properties.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 17,
                "name": "Basil",
                "scientific_name": "Ocimum basilicum",
                "image": "https://images.unsplash.com/photo-1618375569909-3c8616cf7733?w=400",
                "watering_frequency": "Daily during hot weather",
                "watering_times": ["Morning"],
                "sunlight": "Full",
                "soil": "Rich, well-draining soil",
                "fertilizer": "Balanced liquid fertilizer every 2 weeks",
                "growth_type": "Pot",
                "care_tips": "Pinch off flower buds to promote leaf growth. Harvest regularly. Essential culinary herb.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 18,
                "name": "Jasmine",
                "scientific_name": "Jasminum spp.",
                "image": "https://images.unsplash.com/photo-1584888444406-d2e5e0b5e0b7?w=400",
                "watering_frequency": "Daily during growing season",
                "watering_times": ["Morning", "Evening"],
                "sunlight": "Full to Partial",
                "soil": "Rich, well-draining soil",
                "fertilizer": "High-phosphorus fertilizer during blooming",
                "growth_type": "Open Space or Large Pot",
                "care_tips": "Highly fragrant flowers. Needs support for climbing varieties. Prune after flowering season.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 19,
                "name": "Neem",
                "scientific_name": "Azadirachta indica",
                "image": "https://images.unsplash.com/photo-1588336969754-0b1f52e8bcfa?w=400",
                "watering_frequency": "2-3 times weekly",
                "watering_times": ["Morning"],
                "sunlight": "Full",
                "soil": "Well-draining soil, tolerates poor soil",
                "fertilizer": "Organic compost annually",
                "growth_type": "Open Space",
                "care_tips": "Natural pesticide plant. Medicinal properties. Drought-tolerant once established. Can grow quite large.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            },
            {
                "id": 20,
                "name": "Rubber Plant",
                "scientific_name": "Ficus elastica",
                "image": "https://images.unsplash.com/photo-1597166754768-28bb7e3cc49a?w=400",
                "watering_frequency": "Once weekly",
                "watering_times": ["Morning"],
                "sunlight": "Partial to Full",
                "soil": "Well-draining potting mix",
                "fertilizer": "Balanced liquid fertilizer monthly in growing season",
                "growth_type": "Pot",
                "care_tips": "Wipe leaves with damp cloth to remove dust. Can grow quite tall indoors. Tolerates some neglect.",
                "saved": False,
                "last_watered": None,
                "watering_status": {"morning": False, "evening": False}
            }
        ]
        
        with open(PLANTS_FILE, 'w') as f:
            json.dump(default_plants, f, indent=2)

def load_plants():
    """Load plants from JSON file"""
    with open(PLANTS_FILE, 'r') as f:
        return json.load(f)

def save_plants(plants):
    """Save plants to JSON file"""
    with open(PLANTS_FILE, 'w') as f:
        json.dump(plants, f, indent=2)

# Initialize plants data on startup
initialize_plants_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_plants', methods=['GET'])
def get_plants():
    """Return all plants"""
    plants = load_plants()
    return jsonify(plants)

@app.route('/add_plant', methods=['POST'])
def add_plant():
    """Add a new plant"""
    data = request.json
    plants = load_plants()
    
    # Generate new ID
    new_id = max([p['id'] for p in plants]) + 1 if plants else 1
    
    new_plant = {
        "id": new_id,
        "name": data.get('name'),
        "scientific_name": data.get('scientific_name', ''),
        "image": data.get('image', ''),
        "watering_frequency": data.get('watering_frequency', ''),
        "watering_times": data.get('watering_times', []),
        "sunlight": data.get('sunlight', ''),
        "soil": data.get('soil', ''),
        "fertilizer": data.get('fertilizer', ''),
        "growth_type": data.get('growth_type', ''),
        "care_tips": data.get('care_tips', ''),
        "saved": data.get('saved', False),
        "last_watered": None,
        "watering_status": {"morning": False, "evening": False}
    }
    
    plants.append(new_plant)
    save_plants(plants)
    
    return jsonify({"success": True, "plant": new_plant})

@app.route('/save_to_garden/<int:plant_id>', methods=['POST'])
def save_to_garden(plant_id):
    """Save a plant to user's garden"""
    plants = load_plants()
    
    for plant in plants:
        if plant['id'] == plant_id:
            plant['saved'] = True
            save_plants(plants)
            return jsonify({"success": True, "message": "Plant saved to garden"})
    
    return jsonify({"success": False, "message": "Plant not found"}), 404

@app.route('/remove_from_garden/<int:plant_id>', methods=['POST'])
def remove_from_garden(plant_id):
    """Remove a plant from user's garden"""
    plants = load_plants()
    
    for plant in plants:
        if plant['id'] == plant_id:
            plant['saved'] = False
            plant['watering_status'] = {"morning": False, "evening": False}
            save_plants(plants)
            return jsonify({"success": True, "message": "Plant removed from garden"})
    
    return jsonify({"success": False, "message": "Plant not found"}), 404

@app.route('/update_watering/<int:plant_id>', methods=['POST'])
def update_watering(plant_id):
    """Update watering status for a plant"""
    data = request.json
    time_of_day = data.get('time_of_day')  # 'morning' or 'evening'
    
    plants = load_plants()
    
    for plant in plants:
        if plant['id'] == plant_id:
            plant['watering_status'][time_of_day] = True
            plant['last_watered'] = datetime.now().isoformat()
            save_plants(plants)
            return jsonify({"success": True, "message": f"{time_of_day.capitalize()} watering recorded"})
    
    return jsonify({"success": False, "message": "Plant not found"}), 404

@app.route('/reset_watering_status', methods=['POST'])
def reset_watering_status():
    """Reset all watering statuses (can be called daily)"""
    plants = load_plants()
    
    for plant in plants:
        plant['watering_status'] = {"morning": False, "evening": False}
    
    save_plants(plants)
    return jsonify({"success": True, "message": "Watering statuses reset"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)