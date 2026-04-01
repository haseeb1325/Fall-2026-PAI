from flask import Flask, render_template, request, jsonify
import difflib

app = Flask(__name__)


qa_pairs = {
    # Greetings 
    "hi": "Hi there! 👋 Welcome to TravelMate — your friendly travel companion.",
    "hello": "Hello! 🌍 Where are you planning to travel today?",
    "how are you": "I’m awesome 😄 — ready to plan your next adventure!",
    "good morning": "Good morning! ☀️ Planning a trip somewhere beautiful?",
    "good night": "Good night 🌙, see you on your next journey!",
    "thank you": "You're welcome! 😊 Happy to help anytime.",
    "bye": "Goodbye! 🌏 Safe travels and enjoy your journey.",

    # Weather (Pakistan) 
    "lahore weather": "Lahore weather is mostly warm 🌤️ around 30°C these days.",
    "karachi weather": "Karachi is hot and humid ☀️ around 32°C.",
    "islamabad weather": "Islamabad weather is pleasant 🌳 around 24°C — perfect for sightseeing.",
    "murree weather": "Murree is cool 🌧️ around 15°C — carry a light jacket.",
    "hunza weather": "Hunza is breezy and fresh 🌄 around 14°C.",
    "faisalabad weather": "Faisalabad has moderate weather ☁️ around 27°C.",
    "skardu weather": "Skardu is cold ❄️ around 10°C — great for mountain lovers.",
    "multan weather": "Multan is very hot 🔥 around 36°C — known for its dry climate.",
    "sialkot weather": "Sialkot is moderate 🌤️ around 29°C — ideal for travel.",
    "peshawar weather": "Peshawar has warm weather 🌞 around 31°C.",
    "quetta weather": "Quetta is cool and dry 🏔️ around 18°C.",
    "sukkur weather": "Sukkur is hot ☀️ around 35°C — near the Indus River.",

    # Famous Places (Pakistan) 
    "lahore famous places": "Lahore: Badshahi Mosque, Lahore Fort, Minar-e-Pakistan, Shalimar Gardens, Food Street.",
    "karachi famous places": "Karachi: Clifton Beach, Mazar-e-Quaid, Dolmen Mall, French Beach, Maritime Museum.",
    "islamabad famous places": "Islamabad: Faisal Mosque, Daman-e-Koh, Rawal Lake, Lok Virsa, Centaurus Mall.",
    "murree famous places": "Murree: Mall Road, Kashmir Point, Patriata, Pindi Point.",
    "hunza famous places": "Hunza: Baltit Fort, Altit Fort, Attabad Lake, Passu Cones, Karimabad.",
    "faisalabad famous places": "Faisalabad: Ghanta Ghar, Jinnah Garden, Lyallpur Museum, Chenab Club.",
    "skardu famous places": "Skardu: Shangrila Resort, Satpara Lake, Kharpocho Fort, Shigar Fort.",
    "multan famous places": "Multan: Shah Rukn-e-Alam Tomb, Multan Fort, Hussain Agahi Bazaar, Shrine of Bahauddin Zakariya.",
    "sialkot famous places": "Sialkot: Iqbal Manzil, Sialkot Fort, Marala Headworks, Clock Tower.",
    "peshawar famous places": "Peshawar: Qissa Khwani Bazaar, Bala Hisar Fort, Mahabat Khan Mosque, Peshawar Museum.",
    "quetta famous places": "Quetta: Hanna Lake, Quaid-e-Azam Residency, Hazarganji National Park, Urak Valley.",
    "sukkur famous places": "Sukkur: Lansdowne Bridge, Sukkur Barrage, Sadhu Belo Temple, Lab-e-Mehran Park.",

    # Hotels 
    "lahore hotels": "Top Lahore hotels: Avari, Pearl Continental, Hotel One, Nishat Hotel.",
    "karachi hotels": "Karachi hotels: Marriott, Movenpick, Beach Luxury, Pearl Continental.",
    "islamabad hotels": "Islamabad hotels: Serena Hotel, Ramada, Hotel Margala, Centaurus Suites.",
    "murree hotels": "Murree hotels: Hotel One, Grand Taj, Pearl Continental Bhurban.",
    "hunza hotels": "Hunza hotels: Luxus Hunza, Serena Inn, Darbar Hotel.",
    "faisalabad hotels": "Faisalabad hotels: Faisalabad Serena, Hotel One, Grand Regent.",
    "skardu hotels": "Skardu hotels: Serena Shigar Fort, Shangrila Resort, Hotel Reego.",
    "multan hotels": "Multan hotels: Ramada, Avari Xpress, Hotel Grace Inn.",
    "sialkot hotels": "Sialkot hotels: Hotel One, Javson Hotel, The Hotel Chenab.",
    "peshawar hotels": "Peshawar hotels: Shelton’s Rezidor, Pearl Continental, Fort Continental.",
    "quetta hotels": "Quetta hotels: Serena Hotel, Bloom Star, Quetta Palace Hotel.",

    # Food
    "lahore food": "Lahore food: Butt Karahi, Andaaz, Haveli, Food Street delights 🍗.",
    "karachi food": "Karachi food: Kolachi, BBQ Tonight, Do Darya 🍤.",
    "islamabad food": "Islamabad food: Monal, Chaaye Khana, Savour Foods 🍛.",
    "murree food": "Murree food: Red Onion, Usmania, Second Cup Café ☕.",
    "hunza food": "Hunza food: Café de Hunza, Glacier Breeze 🍲.",
    "faisalabad food": "Faisalabad food: Bundu Khan, Salt’n Pepper, Forks n Knives 🍕.",
    "skardu food": "Skardu food: Mountain Lodge Café, Tibet Motel Restaurant 🏔️.",
    "multan food": "Multan food: Sohan Halwa, Shahjahan Grill, Bundu Khan 🍖.",
    "sialkot food": "Sialkot food: London Café, Salt’n Pepper Village, Grill House.",
    "peshawar food": "Peshawar food: Namak Mandi Karahi, Jalil Kabab House 🍢.",
    "quetta food": "Quetta food: Sajji House, Serena Café, Lehri Sajji 🍗.",
    "sukkur food": "Sukkur food: Café Sajawal, Al Habib Restaurant, Khairpur Sweets 🍛.",

    # Travel Info
    "distance lahore islamabad": "Lahore → Islamabad: 380 km (~5 hrs by car).",
    "distance islamabad murree": "Islamabad → Murree: 60 km (~1.5 hrs).",
    "distance gilgit hunza": "Gilgit → Hunza: 100 km (~2 hrs).",
    "distance karachi lahore": "Karachi → Lahore: 1200 km (~1.5 hr flight or 18 hrs road).",
    "distance multan lahore": "Multan → Lahore: 340 km (~4 hrs).",
    "distance peshawar islamabad": "Peshawar → Islamabad: 180 km (~2 hrs).",
    "distance quetta karachi": "Quetta → Karachi: 700 km (~9 hrs).",

    # General Pakistan Info
    "contact": "Tourist Helpline ☎️ 1422 — available 24/7 across Pakistan.",
    "currency": "Currency: Pakistani Rupee (PKR). 1 USD ≈ 280 PKR.",
    "emergency": "Emergency Numbers: Police 15 | Ambulance 1122 | Fire 16 🚨",
    "language": "Languages: Urdu (national), English widely spoken.",
    "visa": "Tourist visa required for most countries. Visit visa.gov.pk 🌐",
    "safety": "Pakistan’s major tourist areas are safe 👍 — just avoid remote travel at night.",
    "festival": "Famous festivals: Basant, Shandur Polo, Independence Day 🇵🇰",
    "shopping": "Shopping: Emporium (Lahore), Dolmen Mall (Karachi), Centaurus (Islamabad).",
    "transport": "Transport: Daewoo, Faisal Movers, Careem, InDrive 🚗.",
    "airport": "Airports: Jinnah Intl (Karachi), Allama Iqbal (Lahore), Islamabad Intl ✈️.",
    "internet": "Free WiFi in hotels, cafes, airports 📶.",
    "best time": "Best months: March–May & Sept–Nov (pleasant weather).",
    "mountains": "Mountains: Try Hunza, Skardu, Fairy Meadows, Naran, Kaghan 🏔️.",

    # International Countries 
    "uae famous places": "UAE 🇦🇪: Burj Khalifa, Dubai Mall, Palm Jumeirah, Sheikh Zayed Mosque.",
    "turkey famous places": "Turkey 🇹🇷: Hagia Sophia, Cappadocia, Blue Mosque, Pamukkale.",
    "malaysia famous places": "Malaysia 🇲🇾: Petronas Towers, Langkawi, Batu Caves, Penang Island.",
    "uk famous places": "UK 🇬🇧: Big Ben, Buckingham Palace, London Eye, Stonehenge.",
    "usa famous places": "USA 🇺🇸: Statue of Liberty, Grand Canyon, Times Square, Yellowstone Park.",
    "saudi arabia famous places": "Saudi Arabia 🇸🇦: Makkah, Madinah, Riyadh Kingdom Tower, Al Ula.",
    "japan famous places": "Japan 🇯🇵: Tokyo Tower, Mount Fuji, Kyoto Temples, Osaka Castle.",
    "china famous places": "China 🇨🇳: Great Wall, Forbidden City, Shanghai Tower, Terracotta Army.",
    "france famous places": "France 🇫🇷: Eiffel Tower, Louvre Museum, Nice Beach, Versailles Palace.",
    "italy famous places": "Italy 🇮🇹: Colosseum, Venice Canals, Leaning Tower of Pisa, Amalfi Coast.",
    "thailand famous places": "Thailand 🇹🇭: Phuket, Bangkok Temples, Chiang Mai, Phi Phi Islands.",
    "indonesia famous places": "Indonesia 🇮🇩: Bali, Jakarta, Komodo Island, Borobudur Temple."
}


# 2️⃣ Famous Places Detailed Info

place_details = {
    # Lahore
    "badshahi mosque": "📍 Lahore | Built in 1673 by Emperor Aurangzeb. Entry Free. Famous for Mughal architecture & red sandstone.",
    "lahore fort": "📍 Lahore | UNESCO World Heritage Site. Entry ~PKR 50. Famous for Sheesh Mahal & royal chambers.",
    "minar e pakistan": "📍 Lahore | Historical monument built in 1968 where Pakistan Resolution was passed. Entry Free.",
    "shalimar gardens": "📍 Lahore | Mughal-era terraced garden built by Shah Jahan. Entry ~PKR 20. Known for fountains & floral beauty.",
    "food street": "📍 Lahore | Near Badshahi Mosque. Famous for Lahori food like Karahi, Seekh Kabab, and Halwa Puri. Open till late night.",

    # Karachi
    "clifton beach": "📍 Karachi | Popular sea view for camel rides & sunsets 🌅. Free entry.",
    "mazar e quaid": "📍 Karachi | Tomb of Quaid-e-Azam Muhammad Ali Jinnah. Entry Free. Historical landmark.",
    "dolmen mall": "📍 Karachi | High-end shopping mall with branded outlets & sea view restaurants.",
    "french beach": "📍 Karachi | Private beach for families & tourists. Entry ~PKR 1000. Great for swimming & picnics.",
    "maritime museum": "📍 Karachi | Navy-managed museum. Entry ~PKR 100. Features submarines & aircraft exhibits.",

    # Islamabad 
    "faisal mosque": "📍 Islamabad | Largest mosque in Pakistan. Entry Free. Stunning modern Islamic architecture.",
    "daman e koh": "📍 Islamabad | Hilltop viewpoint in Margalla Hills 🌄. Free entry. Perfect for sunset views.",
    "rawal lake": "📍 Islamabad | Artificial lake with boating. Charges ~PKR 500. Great picnic spot.",
    "lok virsa": "📍 Islamabad | Heritage museum showcasing Pakistani culture & traditions. Entry ~PKR 250.",
    "centaurus mall": "📍 Islamabad | Famous shopping & dining center with cinemas and international brands.",

    # Murree 
    "mall road": "📍 Murree | Main shopping street 🛍️. Best for handicrafts & traditional food.",
    "kashmir point": "📍 Murree | Scenic viewpoint of snow-capped mountains. Free entry.",
    "patriata": "📍 Murree | Also known as New Murree. Chairlift & cable car rides 🎢. Ticket ~PKR 900.",
    "pindi point": "📍 Murree | Viewpoint with chairlift & pine forest views 🌲. Entry ~PKR 100.",

    # Hunza
    "baltit fort": "📍 Hunza | 700-year-old fort in Karimabad. Ticket ~PKR 400. Scenic mountain backdrop 🏔️.",
    "altit fort": "📍 Hunza | 900-year-old fort. Ticket ~PKR 300. Restored cultural site.",
    "attabad lake": "📍 Hunza | Formed after 2010 landslide. Boating charges ~PKR 1000. Stunning turquoise water 💙.",
    "passu cones": "📍 Hunza | Iconic pointed mountain peaks. Free entry. Popular for photography 📸.",
    "karimabad": "📍 Hunza | Central town with cafes & bazaars. Base for exploring forts & valleys.",

    # Faisalabad 
    "ghanta ghar": "📍 Faisalabad | Central clock tower built in 1903. Surrounded by 8 bazaars forming Union Jack shape.",
    "jinnah garden": "📍 Faisalabad | City’s main park 🌳. Free entry. Great for family outings.",
    "lyallpur museum": "📍 Faisalabad | Chronicles city’s history. Entry ~PKR 100. Displays cultural artifacts.",
    "chenab club": "📍 Faisalabad | Elite social club with restaurants, gym & swimming pool facilities.",

    # Multan
    "shah rukn e alam tomb": "📍 Multan | Built in 1324. Entry Free. Tomb of famous Sufi saint Shah Rukn-e-Alam.",
    "multan fort": "📍 Multan | Ancient fort offering city view. Entry ~PKR 50. Historical architecture.",
    "hussain agahi bazaar": "📍 Multan | Famous for handicrafts, blue pottery, and Multani Sohan Halwa.",
    "bahauddin zakariya shrine": "📍 Multan | 13th-century shrine of Sufi saint Bahauddin Zakariya. Free entry.",

    # Sialkot
    "iqbal manzil": "📍 Sialkot | Birthplace of Allama Iqbal. Entry Free. Preserved as a heritage museum.",
    "sialkot fort": "📍 Sialkot | Ancient fort ruins with city view. Entry Free.",
    "marala headworks": "📍 Sialkot | Picnic spot on Chenab River. Free entry. Boating & fishing available.",
    "clock tower sialkot": "📍 Sialkot | Historical landmark in city center.",

    # Peshawar
    "qissa khwani bazaar": "📍 Peshawar | Historic market known for traditional food and handicrafts.",
    "bala hisar fort": "📍 Peshawar | Built in 1562 by Mughal emperor. Entry ~PKR 50.",
    "mahabat khan mosque": "📍 Peshawar | 17th-century Mughal mosque. Entry Free.",
    "peshawar museum": "📍 Peshawar | Houses Gandhara art & Buddhist relics. Entry ~PKR 100.",

    # Quetta
    "hanna lake": "📍 Quetta | Scenic turquoise lake surrounded by mountains. Boating available. Entry ~PKR 200.",
    "quaid e azam residency": "📍 Ziarat (near Quetta) | Quaid-e-Azam’s summer home. Entry Free.",
    "hazarganji park": "📍 Quetta | National park with rare Chilghoza pine trees 🌲. Entry ~PKR 150.",
    "urak valley": "📍 Quetta | Known for apple orchards 🍎 & cool breeze.",

    # Sukkur
    "lansdowne bridge": "📍 Sukkur | Historic iron bridge (1889). Engineering marvel over Indus River.",
    "sukkur barrage": "📍 Sukkur | 1932 irrigation system. Great view at sunset 🌅.",
    "sadhu belo temple": "📍 Sukkur | Hindu temple on island in Indus River. Access via boat ⛵.",
    "lab e mehran park": "📍 Sukkur | Beautiful riverside park ideal for evening walks.",

    # Skardu
    "shangrila resort": "📍 Skardu | Known as ‘Heaven on Earth’. Entry PKR 500. Lakeside resort with boat rides.",
    "satpara lake": "📍 Skardu | Freshwater lake near Skardu city. Boating available. Surrounded by mountains.",
    "kharpocho fort": "📍 Skardu | Built in 16th century by Ali Sher Khan. Great panoramic view of the valley.",
    "shigar fort": "📍 Skardu | 400-year-old fort converted into a heritage hotel. Entry ~PKR 500.",

    # International Landmarks
    "burj khalifa": "📍 Dubai, UAE | Tallest building in the world 🌆. Entry ~AED 150. Amazing observation deck views.",
    "hagia sophia": "📍 Istanbul, Turkey | Former church & mosque. Entry ~TRY 300. Rich history & mosaics.",
    "petronas towers": "📍 Kuala Lumpur, Malaysia | Twin skyscrapers. Entry ~MYR 80. Skybridge access available.",
    "big ben": "📍 London, UK | Famous clock tower near Westminster Abbey ⏰.",
    "statue of liberty": "📍 New York, USA | Symbol of freedom. Ferry ticket ~$25.",
    "makkah": "📍 Saudi Arabia | Holiest city in Islam. Access for Muslims only.",
    "mount fuji": "📍 Japan | Iconic mountain 🗻. Hiking season July–Sept.",
    "great wall of china": "📍 Beijing, China | 21,000 km long. Entry ~CNY 40.",
    "eiffel tower": "📍 Paris, France | World landmark. Entry ~€20. Best view at night 🌃.",
    "colosseum": "📍 Rome, Italy | Ancient Roman amphitheater. Entry ~€18.",
    "phuket": "📍 Thailand | Famous island 🏝️ with beaches, nightlife & diving.",
    "bali": "📍 Indonesia | Tropical paradise 🌴 with temples & beaches."
}



def get_response(user_input):
    user_input = user_input.lower().strip()

    # If empty message
    if not user_input:
        return "Please type something 😊 I’m here to help you with travel info!"

    # 🔹 A. Check for specific famous place
    for place, info in place_details.items():
        if place in user_input:
            return info

    # 🔹 B. Check for direct or partial match in qa_pairs
    for key, answer in qa_pairs.items():
        if key in user_input:
            return answer

    # 🔹 C. Try fuzzy match if partial text is similar
    best_match = difflib.get_close_matches(user_input, qa_pairs.keys(), n=1, cutoff=0.6)
    if best_match:
        return qa_pairs[best_match[0]]

    # 🔹 D. Default if no match found at all
    return "Hmm 🤔 I don’t have that info yet. Try asking about a city, weather, famous places, or a specific landmark!"



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_msg = request.form["msg"]
    response = get_response(user_msg)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)