import sqlite3

conn = sqlite3.connect("treetrace.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS trees (
    tree_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    scientific_name TEXT,
    family TEXT,
    category TEXT,
    description TEXT,
    age INTEGER,
    location TEXT,
    benefits TEXT,
    uses TEXT,
    parts_used TEXT,
    health_status TEXT,
    maintenance_status TEXT,
    planting_date TEXT,
    photo TEXT
)
""")

trees = [
    ('T001', 'Neem', 'Azadirachta indica', 'Meliaceae', 'Medicinal Tree',
     'A useful evergreen tree known for its medicinal and environmental benefits.',
     15, 'Express Botanical Garden',
     'Supports skin health, traditional medicine and natural pest control.',
     'Medicinal products, natural pesticides and environmental applications.',
     'Leaves, bark, seeds and neem oil', 'Healthy', 'Regular Watering',
     '2011-06-15', None),

    ('T002', 'Amla', 'Phyllanthus emblica', 'Phyllanthaceae', 'Medicinal Tree',
     'Amla is a nutrient-rich tree widely used in traditional medicine.',
     12, 'Express Botanical Garden',
     'Rich in vitamin C and supports general wellness.',
     'Food products, traditional medicine and herbal preparations.',
     'Fruit, leaves and bark', 'Healthy', 'Regular Watering',
     '2014-06-15', None),

    ('T003', 'Ashoka', 'Saraca asoca', 'Fabaceae', 'Medicinal Tree',
     'A flowering tree valued for its medicinal and ornamental importance.',
     14, 'Express Botanical Garden',
     'Traditionally associated with women health and herbal medicine.',
     'Traditional medicine and ornamental planting.',
     'Bark, flowers and leaves', 'Healthy', 'Regular Watering',
     '2012-06-15', None),

    ('T004', 'Arjun', 'Terminalia arjuna', 'Combretaceae', 'Medicinal Tree',
     'A large tree traditionally valued for its medicinal properties.',
     16, 'Express Botanical Garden',
     'Traditionally used in herbal preparations and heart-health formulations.',
     'Ayurvedic and herbal applications.',
     'Bark, leaves and fruits', 'Healthy', 'Regular Watering',
     '2010-06-15', None),

    ('T005', 'Bael', 'Aegle marmelos', 'Rutaceae', 'Medicinal Tree',
     'A hardy tree known for its fruit and traditional medicinal uses.',
     13, 'Express Botanical Garden',
     'Supports traditional digestive and wellness applications.',
     'Food, beverages and traditional medicine.',
     'Fruit, leaves and bark', 'Healthy', 'Regular Watering',
     '2013-06-15', None),

    ('T006', 'Jamun', 'Syzygium cumini', 'Myrtaceae', 'Fruit Tree',
     'A fruit-bearing evergreen tree commonly found in tropical regions.',
     14, 'Express Botanical Garden',
     'Provides nutritious fruits and supports biodiversity.',
     'Fresh fruit, beverages and traditional preparations.',
     'Fruit, seeds and bark', 'Healthy', 'Regular Watering',
     '2012-06-15', None),

    ('T007', 'Giloy', 'Tinospora cordifolia', 'Menispermaceae', 'Medicinal Plant',
     'A climbing medicinal plant widely used in traditional herbal practices.',
     8, 'Express Botanical Garden',
     'Traditionally used in herbal wellness preparations.',
     'Ayurvedic and herbal preparations.',
     'Stem and leaves', 'Healthy', 'Regular Watering',
     '2018-06-15', None),

    ('T008', 'Haritaki', 'Terminalia chebula', 'Combretaceae', 'Medicinal Tree',
     'A medicinal tree whose fruit is important in traditional medicine.',
     15, 'Express Botanical Garden',
     'Traditionally used for digestive and wellness applications.',
     'Herbal medicines and traditional preparations.',
     'Fruit, bark and leaves', 'Healthy', 'Regular Watering',
     '2011-06-15', None),

    ('T009', 'Bahera', 'Terminalia bellirica', 'Combretaceae', 'Medicinal Tree',
     'A large tree valued for its fruit and traditional medicinal uses.',
     15, 'Express Botanical Garden',
     'Used traditionally in herbal and wellness preparations.',
     'Traditional medicine and herbal products.',
     'Fruit, bark and leaves', 'Healthy', 'Regular Watering',
     '2011-06-15', None),

    ('T010', 'Moringa', 'Moringa oleifera', 'Moringaceae', 'Medicinal/Food Tree',
     'A fast-growing tree known for its nutritious leaves and pods.',
     10, 'Express Botanical Garden',
     'Leaves and pods provide important nutritional value.',
     'Food, nutritional products and traditional medicine.',
     'Leaves, pods, seeds and bark', 'Healthy', 'Regular Watering',
     '2016-06-15', None),

    ('T011', 'Tulsi', 'Ocimum tenuiflorum', 'Lamiaceae', 'Medicinal Plant',
     'An aromatic medicinal plant commonly used in traditional practices.',
     5, 'Express Botanical Garden',
     'Traditionally used in herbal and wellness preparations.',
     'Herbal preparations, beverages and traditional medicine.',
     'Leaves and stems', 'Healthy', 'Regular Watering',
     '2021-06-15', None),

    ('T012', 'Saptaparni', 'Alstonia scholaris', 'Apocynaceae', 'Medicinal Tree',
     'An evergreen tree known for its distinctive whorled leaves.',
     17, 'Express Botanical Garden',
     'Provides shade and contributes to the local ecosystem.',
     'Traditional medicine and environmental uses.',
     'Bark, leaves and flowers', 'Healthy', 'Regular Watering',
     '2009-06-15', None),

    ('T013', 'Shisham', 'Dalbergia sissoo', 'Fabaceae', 'Timber Tree',
     'A valuable deciduous tree known for its strong wood.',
     18, 'Express Botanical Garden',
     'Provides shade, habitat and environmental benefits.',
     'Timber, furniture and woodworking.',
     'Wood, leaves and bark', 'Healthy', 'Regular Watering',
     '2008-06-15', None),

    ('T014', 'Karanja', 'Pongamia pinnata', 'Fabaceae', 'Medicinal/Environmental Tree',
     'A hardy tree valued for its environmental and traditional uses.',
     16, 'Express Botanical Garden',
     'Supports soil improvement and provides useful seeds.',
     'Biofuel research, traditional medicine and environmental applications.',
     'Seeds, leaves and bark', 'Healthy', 'Regular Watering',
     '2010-06-15', None),

    ('T015', 'Banyan', 'Ficus benghalensis', 'Moraceae', 'Native Tree',
     'A large long-lived tree with extensive aerial roots and a broad canopy.',
     25, 'Express Botanical Garden',
     'Provides shade, habitat and supports local biodiversity.',
     'Shade, ecological applications and traditional uses.',
     'Bark, leaves, roots and fruits', 'Healthy', 'Regular Watering',
     '2001-06-15', None)
]

cursor.executemany("""
INSERT OR REPLACE INTO trees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", trees)

conn.commit()
conn.close()

print("All 15 tree records inserted successfully!")