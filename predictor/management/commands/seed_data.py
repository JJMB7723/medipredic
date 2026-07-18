import os
from django.core.management.base import BaseCommand
from predictor.models import Disease
from medicines.models import Medicine

class Command(BaseCommand):
    help = "Seed the database with 41 diseases, precautions, descriptions, and recommended medications."

    def handle(self, *args, **options):
        self.stdout.write("[*] Seeding database with diseases and medications...")

        diseases_data = {
            "Fungal infection": {
                "description": "A skin infection caused by a fungus. Common types include athlete's foot, jock itch, and ringworm. Fungi thrive in warm, moist environments.",
                "causes": "Overgrowth of fungi due to poor hygiene, high humidity, wearing tight damp clothing, or compromised immunity.",
                "precautions": "bath twice, use dettol or antiseptic soap, keep skin dry and clean, do not share towels or clothes",
                "specialist": "Dermatologist",
                "medicines": [
                    {"name": "Clotrimazole Cream", "dosage": "Apply thin layer to affected area twice daily for 2-4 weeks.", "side_effects": "Mild burning, redness, skin irritation.", "warnings": "Avoid contact with eyes. Discontinue if severe irritation occurs."},
                    {"name": "Fluconazole 150mg", "dosage": "One capsule orally as a single dose.", "side_effects": "Headache, nausea, abdominal pain.", "warnings": "Consult doctor if pregnant or having liver/kidney disease."}
                ]
            },
            "Allergy": {
                "description": "An immune system reaction to a foreign substance (allergen) that is typically not harmful to most people, such as pollen, pet dander, or food.",
                "causes": "Hypersensitivity of the immune system leading to release of histamines upon exposure to dust, pollen, certain foods, or insect stings.",
                "precautions": "avoid allergens, keep environment dust-free, use air purifiers, wear masks outdoors",
                "specialist": "Allergist / Immunologist",
                "medicines": [
                    {"name": "Cetirizine 10mg", "dosage": "One tablet daily in the evening.", "side_effects": "Drowsiness, dry mouth, fatigue.", "warnings": "Avoid alcohol and operating heavy machinery."},
                    {"name": "Fluticasone Nasal Spray", "dosage": "1 to 2 sprays in each nostril daily.", "side_effects": "Nasal dryness, headache, throat irritation.", "warnings": "Do not use continuously for more than a few weeks without consulting a doctor."}
                ]
            },
            "GERD": {
                "description": "Gastroesophageal Reflux Disease (acid reflux) is a chronic digestive disease where stomach acid or bile flows back into the food pipe, irritating the lining.",
                "causes": "Weakness or relaxation of the lower esophageal sphincter (LES), smoking, obesity, large meals, or lying down immediately after eating.",
                "precautions": "avoid spicy/fatty foods, eat small frequent meals, do not lie down immediately after eating, sleep with head elevated",
                "specialist": "Gastroenterologist",
                "medicines": [
                    {"name": "Omeprazole 20mg", "dosage": "One capsule daily 30 minutes before breakfast.", "side_effects": "Headache, diarrhea, flatulence.", "warnings": "Long term use can affect magnesium absorption."},
                    {"name": "Antacid Gel / Suspension", "dosage": "10-20ml after meals and at bedtime.", "side_effects": "Constipation or diarrhea depending on formulation.", "warnings": "Do not take within 2 hours of other medications."}
                ]
            },
            "Chronic cholestasis": {
                "description": "A condition where the flow of bile from the liver is reduced or stalled, leading to build-up of bile acids and bilirubin in the blood and tissues.",
                "causes": "Liver disease, bile duct obstruction, certain genetic factors, or drug-induced liver injury.",
                "precautions": "avoid alcohol, limit fat intake, stay hydrated, take prescribed vitamin supplements",
                "specialist": "Hepatologist / Gastroenterologist",
                "medicines": [
                    {"name": "Ursodeoxycholic Acid 300mg", "dosage": "One tablet two to three times daily with food.", "side_effects": "Diarrhea, nausea, dry skin.", "warnings": "Regular liver function tests required."},
                    {"name": "Cholestyramine 4g", "dosage": "One sachet mixed with water 1-2 times daily.", "side_effects": "Constipation, bloating, gas.", "warnings": "Take other medications at least 1 hour before or 4-6 hours after."}
                ]
            },
            "Drug Reaction": {
                "description": "An adverse and unintended response to a medication, ranging from mild skin rashes to life-threatening conditions like anaphylaxis.",
                "causes": "Immune system response to a medication or severe side effect due to drug-drug interaction or dosage issues.",
                "precautions": "stop taking the drug immediately, consult doctor, keep a record of the drug name, drink plenty of water",
                "specialist": "Allergist / Dermatologist",
                "medicines": [
                    {"name": "Prednisolone 5mg", "dosage": "As prescribed by physician (usually tapered over days).", "side_effects": "Increased appetite, mood changes, fluid retention.", "warnings": "Do not stop abruptly if taken long term."},
                    {"name": "Fexofenadine 120mg", "dosage": "One tablet daily.", "side_effects": "Drowsiness (rare), dry mouth, headache.", "warnings": "Avoid drinking fruit juices within 2 hours of taking."}
                ]
            },
            "Peptic ulcer disease": {
                "description": "Sores or ulcers that develop on the inside lining of your stomach, small intestine, or esophagus, causing pain and burning discomfort.",
                "causes": "Helicobacter pylori (H. pylori) bacterial infection, or prolonged use of nonsteroidal anti-inflammatory drugs (NSAIDs) like ibuprofen.",
                "precautions": "avoid NSAIDs/painkillers, avoid spicy foods, limit caffeine and alcohol, manage stress levels",
                "specialist": "Gastroenterologist",
                "medicines": [
                    {"name": "Pantoprazole 40mg", "dosage": "One tablet daily before breakfast.", "side_effects": "Headache, joint pain, diarrhea.", "warnings": "Inform doctor of any unexplained weight loss or blood in stool."},
                    {"name": "Amoxicillin 500mg", "dosage": "One capsule three times daily (if H. pylori positive).", "side_effects": "Nausea, diarrhea, skin rash.", "warnings": "Complete the full antibiotic course."}
                ]
            },
            "AIDS": {
                "description": "Acquired Immunodeficiency Syndrome is a chronic, potentially life-threatening condition caused by the Human Immunodeficiency Virus (HIV) which damages the immune system.",
                "causes": "Infection by the HIV virus, transmitted through unprotected sexual contact, sharing needles, or from mother to child during childbirth/breastfeeding.",
                "precautions": "use protection during intercourse, do not share needles, follow antiretroviral therapy, consult doctor regularly",
                "specialist": "Infectious Disease Specialist",
                "medicines": [
                    {"name": "Tenofovir/Emtricitabine", "dosage": "One tablet daily with or without food.", "side_effects": "Nausea, fatigue, dizziness, kidney function alterations.", "warnings": "Requires close medical supervision and regular lab testing."},
                    {"name": "Dolutegravir 50mg", "dosage": "One tablet daily.", "side_effects": "Insomnia, headache, diarrhea.", "warnings": "Monitor for signs of liver toxicity."}
                ]
            },
            "Diabetes": {
                "description": "A metabolic disease characterized by chronic high blood glucose (sugar) levels due to inadequate insulin production or insulin resistance.",
                "causes": "Genetics, obesity, sedentary lifestyle, pancreatic dysfunction, or autoimmune response (Type 1).",
                "precautions": "restrict sugar/carbohydrate intake, exercise daily, monitor blood glucose levels, take prescribed medication, care for feet",
                "specialist": "Endocrinologist",
                "medicines": [
                    {"name": "Metformin 500mg", "dosage": "One tablet twice daily with meals.", "side_effects": "Nausea, bloating, metallic taste, diarrhea.", "warnings": "Risk of lactic acidosis; avoid heavy alcohol consumption."},
                    {"name": "Glimepiride 2mg", "dosage": "One tablet daily before breakfast.", "side_effects": "Hypoglycemia (low blood sugar), weight gain.", "warnings": "Ensure meals are eaten on time to prevent sudden sugar drops."}
                ]
            },
            "Gastroenteritis": {
                "description": "An inflammation of the lining of the intestines caused by a virus, bacteria, or parasites, commonly referred to as stomach flu.",
                "causes": "Ingestion of contaminated food or water, or contact with an infected person.",
                "precautions": "drink ORS/electrolytes, eat bland food (bananas/rice), wash hands frequently, avoid dairy and oily food",
                "specialist": "General Physician / Gastroenterologist",
                "medicines": [
                    {"name": "ORS (Oral Rehydration Salts)", "dosage": "Dissolve 1 sachet in 1 liter of clean water; drink throughout the day.", "side_effects": "None when mixed and used correctly.", "warnings": "Use boiled/purified water only."},
                    {"name": "Loperamide 2mg", "dosage": "Two capsules initially, followed by one capsule after each loose stool.", "side_effects": "Constipation, dizziness, dry mouth.", "warnings": "Do not use if stool contains blood or if high fever is present."}
                ]
            },
            "Bronchial Asthma": {
                "description": "A chronic disease where the airways in the lungs become inflamed, narrow, and swollen, producing extra mucus, which makes breathing difficult.",
                "causes": "Allergens, respiratory infections, exercise, cold air, smoke, or genetic predisposition.",
                "precautions": "avoid dust/pollen, keep inhaler handy, avoid cold beverages, perform breathing exercises",
                "specialist": "Pulmonologist",
                "medicines": [
                    {"name": "Albuterol Inhaler (Salbutamol)", "dosage": "1 to 2 puffs every 4-6 hours as needed for quick relief.", "side_effects": "Tremors, rapid heart rate, nervousness.", "warnings": "Seek emergency help if symptoms do not improve after use."},
                    {"name": "Montelukast 10mg", "dosage": "One tablet daily in the evening.", "side_effects": "Headache, abdominal pain, mood changes.", "warnings": "Report any unusual behavior changes to doctor."}
                ]
            },
            "Hypertension": {
                "description": "High blood pressure is a common condition in which the long-term force of the blood against artery walls is high enough that it may cause heart disease.",
                "causes": "High salt intake, obesity, stress, genetics, lack of exercise, or kidney dysfunction.",
                "precautions": "reduce salt intake, exercise daily, manage stress, avoid smoking and alcohol, monitor blood pressure",
                "specialist": "Cardiologist",
                "medicines": [
                    {"name": "Amlodipine 5mg", "dosage": "One tablet daily in the morning.", "side_effects": "Swelling of ankles/feet, dizziness, flushing.", "warnings": "Do not stop taking without checking with your doctor."},
                    {"name": "Losartan 50mg", "dosage": "One tablet daily.", "side_effects": "Dizziness, fatigue, back pain.", "warnings": "Contraindicated in pregnancy."}
                ]
            },
            "Migraine": {
                "description": "A neurological condition that causes severe, throbbing headaches, usually on one side of the head, often accompanied by nausea and sensitivity to light/sound.",
                "causes": "Changes in brain chemistry, genetic factors, hormonal fluctuations, stress, bright lights, or certain food triggers.",
                "precautions": "rest in a dark quiet room, avoid loud noises and bright lights, maintain a sleep routine, stay hydrated",
                "specialist": "Neurologist",
                "medicines": [
                    {"name": "Sumatriptan 50mg", "dosage": "One tablet at the onset of migraine pain; can repeat in 2 hours if needed.", "side_effects": "Tingling, pressure in chest/neck, dizziness.", "warnings": "Do not take if you have coronary artery disease."},
                    {"name": "Naproxen 500mg", "dosage": "One tablet twice daily with food.", "side_effects": "Heartburn, nausea, abdominal pain.", "warnings": "Avoid prolonged use due to risk of stomach ulcers."}
                ]
            },
            "Cervical spondylosis": {
                "description": "Age-related wear and tear affecting the spinal disks in your neck. As the disks dehydrate and shrink, signs of osteoarthritis develop.",
                "causes": "Aging, bad posture, repetitive neck strain, neck injuries, or bone spurs in the cervical spine.",
                "precautions": "maintain upright posture, use cervical pillow, perform neck stretching exercises, avoid heavy lifting",
                "specialist": "Orthopedist / Physiotherapist",
                "medicines": [
                    {"name": "Pregabalin 75mg", "dosage": "One capsule daily at bedtime.", "side_effects": "Drowsiness, dizziness, weight gain.", "warnings": "Do not stop taking suddenly."},
                    {"name": "Cyclobenzaprine 10mg", "dosage": "One tablet 2-3 times daily for muscle spasms.", "side_effects": "Drowsiness, dry mouth, tiredness.", "warnings": "Avoid alcohol and activities requiring mental alertness."}
                ]
            },
            "Paralysis (brain hemorrhage)": {
                "description": "Loss of muscle function in a part of the body, often caused by a stroke or rupture of a blood vessel in the brain leading to bleeding.",
                "causes": "Hypertension, ruptured aneurysm, head trauma, blood disorders, or cerebral vascular disease.",
                "precautions": "monitor blood pressure strictly, undergo regular physiotherapy, prevent falls, follow low-sodium diet",
                "specialist": "Neurologist / Neurosurgeon",
                "medicines": [
                    {"name": "Atorvastatin 40mg", "dosage": "One tablet daily at bedtime.", "side_effects": "Muscle pain, headache, liver enzyme changes.", "warnings": "Report unexplained muscle pain/weakness immediately."},
                    {"name": "Citicoline 500mg", "dosage": "One tablet twice daily.", "side_effects": "Insomnia, headache, diarrhea.", "warnings": "Consult neurologist for appropriate recovery protocols."}
                ]
            },
            "Jaundice": {
                "description": "A condition in which the skin, whites of the eyes, and mucous membranes turn yellow because of a high level of bilirubin, a yellow-orange bile pigment.",
                "causes": "Hepatitis, liver disease, gallstones, alcohol abuse, or breakdown of red blood cells.",
                "precautions": "take complete bed rest, consume low-fat boiled diet, drink clean boiled water, avoid physical exertion",
                "specialist": "Hepatologist / Gastroenterologist",
                "medicines": [
                    {"name": "Silymarin 140mg (Milk Thistle)", "dosage": "One capsule three times daily.", "side_effects": "Mild laxative effect, bloating, indigestion.", "warnings": "Supporting treatment only; treat the primary cause of jaundice."},
                    {"name": "Vitamin K1 10mg", "dosage": "As prescribed by doctor (usually in bleeding risk cases).", "side_effects": "Flushing, rapid pulse.", "warnings": "Requires clinical supervision."}
                ]
            },
            "Malaria": {
                "description": "A life-threatening disease caused by plasmodium parasites transmitted through the bites of infected female Anopheles mosquitoes.",
                "causes": "Bite of infected Anopheles mosquito releasing plasmodium parasites into the bloodstream.",
                "precautions": "use mosquito net, apply insect repellent, wear long sleeves, avoid stagnant water around home",
                "specialist": "Infectious Disease Specialist",
                "medicines": [
                    {"name": "Artemether + Lumefantrine", "dosage": "As prescribed (standard course is 4 tablets twice daily for 3 days).", "side_effects": "Headache, dizziness, muscle pain.", "warnings": "Take with fatty food or milk for optimal absorption."},
                    {"name": "Chloroquine 250mg", "dosage": "Dosage depends on regional resistance patterns.", "side_effects": "Nausea, itching, visual disturbances.", "warnings": "Regular eye tests required for long-term usage."}
                ]
            },
            "Chicken pox": {
                "description": "A highly contagious viral infection causing an itchy, blister-like rash on the skin. It is preventable by a vaccine.",
                "causes": "Infection with the Varicella-zoster virus, spread through respiratory droplets or direct contact with the rash.",
                "precautions": "isolate the patient, keep nails short, apply calamine lotion, wear light loose cotton clothes",
                "specialist": "Dermatologist / Pediatrician",
                "medicines": [
                    {"name": "Acyclovir 800mg", "dosage": "One tablet 5 times daily for 5-7 days.", "side_effects": "Nausea, headache, skin rash.", "warnings": "Best if started within 24 hours of rash onset; drink plenty of water."},
                    {"name": "Calamine Lotion", "dosage": "Apply topically to itchy skin rashes as needed.", "side_effects": "Local irritation (rare).", "warnings": "For external use only; do not apply near eyes or open wounds."}
                ]
            },
            "Dengue": {
                "description": "A painful, debilitating mosquito-borne viral disease causing sudden high fever, severe headaches, joint and muscle pain, and rash.",
                "causes": "Infection with the dengue virus, transmitted to humans by the bite of an infected Aedes mosquito.",
                "precautions": "drink plenty of fluids/juices, take complete rest, take paracetamol (avoid aspirin/ibuprofen), monitor platelet count",
                "specialist": "General Physician / Infectious Disease",
                "medicines": [
                    {"name": "Paracetamol 500mg", "dosage": "One tablet every 6 hours as needed for fever and pain.", "side_effects": "Liver damage if taken in excessive quantities.", "warnings": "Do not exceed 4g (4000mg) per day. Avoid NSAIDs (aspirin, ibuprofen) as they increase bleeding risk."},
                    {"name": "Carica Papaya Leaf Extract", "dosage": "One tablet/liquid three times daily to support platelet count.", "side_effects": "Stomach upset (rare).", "warnings": "Should not replace medical care and hydration monitoring."}
                ]
            },
            "Typhoid": {
                "description": "A bacterial infection that can spread throughout the body, affecting many organs. Without prompt treatment, it can cause serious complications.",
                "causes": "Salmonella typhi bacteria, contracted by consuming food or water contaminated with infected feces.",
                "precautions": "drink boiled water, eat thoroughly cooked hot food, isolate patient utensils, wash hands thoroughly",
                "specialist": "Infectious Disease Specialist",
                "medicines": [
                    {"name": "Ciprofloxacin 500mg", "dosage": "One tablet twice daily for 7-14 days.", "side_effects": "Nausea, diarrhea, tendonitis (rare).", "warnings": "Complete the full antibiotic course even if you feel better."},
                    {"name": "Azithromycin 500mg", "dosage": "One tablet daily for 5-7 days.", "side_effects": "Stomach pain, nausea, vomiting.", "warnings": "Report any severe diarrhea to your physician."}
                ]
            },
            "hepatitis A": {
                "description": "A highly contagious liver infection caused by the hepatitis A virus. It is usually self-limiting and does not become chronic.",
                "causes": "Ingestion of contaminated food or water or direct contact with an infectious person.",
                "precautions": "avoid fatty/oily food, wash hands with soap, drink purified water, take adequate bed rest",
                "specialist": "Hepatologist / Gastroenterologist",
                "medicines": [
                    {"name": "Ursodeoxycholic Acid 150mg", "dosage": "One tablet twice daily.", "side_effects": "Diarrhea, skin irritation.", "warnings": "Used to support bile flow during acute liver stress."},
                    {"name": "Vitamin B-Complex Capsule", "dosage": "One capsule daily with food.", "side_effects": "Bright yellow urine (harmless).", "warnings": "Supports nutritional status during recovery."}
                ]
            },
            "Hepatitis B": {
                "description": "A serious liver infection caused by the hepatitis B virus (HBV). It can become chronic, leading to liver failure, cirrhosis, or liver cancer.",
                "causes": "Contact with infectious blood, semen, or other body fluids; sharing needles; or sexual transmission.",
                "precautions": "avoid sharing personal items like razors, use protection, avoid alcohol, take antiviral medications",
                "specialist": "Hepatologist / Gastroenterologist",
                "medicines": [
                    {"name": "Tenofovir Alafenamide 25mg", "dosage": "One tablet daily with food.", "side_effects": "Headache, abdominal pain, nausea.", "warnings": "Requires regular monitoring of bone density and kidney function."},
                    {"name": "Entecavir 0.5mg", "dosage": "One tablet daily on an empty stomach.", "side_effects": "Dizziness, fatigue, nausea.", "warnings": "Do not discontinue abruptly, as this may cause acute hepatitis relapse."}
                ]
            },
            "Hepatitis C": {
                "description": "An infection caused by the hepatitis C virus (HCV) that attacks the liver and leads to inflammation. Most infected people have no symptoms initially.",
                "causes": "Exposure to infected blood, primarily through shared needles, unsterile medical procedures, or blood transfusions.",
                "precautions": "never share needles or syringes, do not donate blood if infected, avoid alcohol completely",
                "specialist": "Hepatologist / Gastroenterologist",
                "medicines": [
                    {"name": "Sofosbuvir/Velpatasvir", "dosage": "One tablet daily for 12 weeks.", "side_effects": "Fatigue, headache, nausea.", "warnings": "Highly effective direct-acting antiviral; complete the full course."},
                    {"name": "Ledipasvir/Sofosbuvir", "dosage": "One tablet daily for 8-12 weeks.", "side_effects": "Fatigue, headache.", "warnings": "Monitor for drug interactions, especially with antacids."}
                ]
            },
            "Hepatitis D": {
                "description": "Also known as delta hepatitis, this is a serious liver disease caused by the hepatitis D virus (HDV) that only occurs in people infected with HBV.",
                "causes": "HDV infection, which requires the helper function of HBV to replicate. Transmitted through contact with blood or body fluids.",
                "precautions": "get vaccinated against Hepatitis B (which prevents HDV), avoid contact with blood, follow strict hygiene",
                "specialist": "Hepatologist / Gastroenterologist",
                "medicines": [
                    {"name": "Pegylated Interferon Alfa-2a", "dosage": "Weekly subcutaneous injection as prescribed.", "side_effects": "Flu-like symptoms, depression, hair thinning.", "warnings": "Requires intense monitoring by a liver specialist."},
                    {"name": "Bulevirtide", "dosage": "Subcutaneous injection daily as prescribed by specialist.", "side_effects": "Headache, injection site reaction.", "warnings": "Relatively new direct-acting antiviral for HDV."}
                ]
            },
            "Hepatitis E": {
                "description": "A liver disease caused by the hepatitis E virus (HEV). It is usually self-limiting but can be fatal in pregnant women.",
                "causes": "Ingestion of fecal-contaminated drinking water, undercooked pork, or wild game.",
                "precautions": "drink boiled or bottled water, cook meat thoroughly, maintain proper hand hygiene, take rest",
                "specialist": "Hepatologist / Gastroenterologist",
                "medicines": [
                    {"name": "Ribavirin 200mg", "dosage": "As prescribed by doctor (usually in chronic or severe cases).", "side_effects": "Anemia, fatigue, rash.", "warnings": "Contraindicated in pregnancy due to severe birth defect risks."},
                    {"name": "Multivitamin Formulation", "dosage": "One capsule daily.", "side_effects": "Mild stomach upset.", "warnings": "Helps maintain overall vitamin status."}
                ]
            },
            "Alcoholic hepatitis": {
                "description": "Inflammation of the liver caused by drinking alcohol. It's most likely to occur in people who drink heavily over many years.",
                "causes": "Chronic heavy alcohol consumption leading to toxic chemical damage and inflammation of liver tissue.",
                "precautions": "stop alcohol consumption completely, follow high-calorie low-sodium diet, consult therapist, stay hydrated",
                "specialist": "Hepatologist / Gastroenterologist",
                "medicines": [
                    {"name": "Prednisolone 40mg", "dosage": "One tablet daily for 28 days (for severe cases).", "side_effects": "Fluid retention, high blood pressure, hyperglycemia.", "warnings": "Contraindicated in active infection or gastrointestinal bleeding."},
                    {"name": "Vitamin B1 (Thiamine) 100mg", "dosage": "One tablet daily.", "side_effects": "Rare mild allergic reactions.", "warnings": "Essential to prevent Wernicke-Korsakoff syndrome in chronic alcohol users."}
                ]
            },
            "Tuberculosis": {
                "description": "A potentially serious infectious disease that mainly affects the lungs. The bacteria are spread from person to person through tiny droplets released into the air.",
                "causes": "Infection by Mycobacterium tuberculosis bacteria.",
                "precautions": "wear masks, ensure ventilation, complete the 6-month DOTS treatment course, separate room",
                "specialist": "Pulmonologist / Infectious Disease",
                "medicines": [
                    {"name": "Isoniazid + Rifampin + Pyrazinamide + Ethambutol", "dosage": "Fixed-dose combination daily as part of DOTS therapy.", "side_effects": "Nausea, orange-colored urine, numbness in feet, joint pain.", "warnings": "Take on empty stomach. Avoid alcohol. Report visual changes or yellow skin immediately."},
                    {"name": "Pyridoxine (Vitamin B6) 20mg", "dosage": "One tablet daily.", "side_effects": "None at therapeutic doses.", "warnings": "Given alongside Isoniazid to prevent peripheral neuropathy."}
                ]
            },
            "Common Cold": {
                "description": "A viral infection of your nose and throat (upper respiratory tract). It's usually harmless, and symptoms disappear in a week or two.",
                "causes": "Rhinovirus or other respiratory viruses, spread through airborne droplets or touching contaminated surfaces.",
                "precautions": "drink warm liquids, gargle with salt water, take rest, cover mouth while sneezing",
                "specialist": "General Physician",
                "medicines": [
                    {"name": "Paracetamol 500mg", "dosage": "One tablet every 6 hours as needed for fever/headache.", "side_effects": "Liver damage if abused.", "warnings": "Do not exceed daily limits."},
                    {"name": "Chlorpheniramine Maleate 4mg", "dosage": "One tablet every 8 hours.", "side_effects": "Drowsiness, dry mouth, blurred vision.", "warnings": "May cause sedation; do not drive."}
                ]
            },
            "Pneumonia": {
                "description": "An infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus, causing cough with phlegm, fever, chills, and difficulty breathing.",
                "causes": "Bacterial (Streptococcus pneumoniae), viral, or fungal infections.",
                "precautions": "stay warm, use humidifier, avoid smoking, complete the prescribed antibiotic course, rest",
                "specialist": "Pulmonologist",
                "medicines": [
                    {"name": "Amoxicillin-Clavulanic Acid 625mg", "dosage": "One tablet twice daily for 7 days.", "side_effects": "Diarrhea, nausea, skin rash.", "warnings": "Do not take if allergic to penicillin."},
                    {"name": "Azithromycin 500mg", "dosage": "One tablet daily for 3 to 5 days.", "side_effects": "Nausea, vomiting, stomach upset.", "warnings": "Inform doctor if you have history of cardiac arrhythmias."}
                ]
            },
            "Dimorphic hemmorhoids(piles)": {
                "description": "Swollen veins in the anus and lower rectum, similar to varicose veins. Can develop inside the rectum (internal) or under the skin around the anus (external).",
                "causes": "Straining during bowel movements, chronic constipation, sitting for long periods, or pregnancy.",
                "precautions": "consume high-fiber diet, drink plenty of water, avoid straining, take warm sitz baths",
                "specialist": "General Surgeon / Proctologist",
                "medicines": [
                    {"name": "Docusate Sodium 100mg", "dosage": "One tablet at bedtime to soften stools.", "side_effects": "Cramping, diarrhea.", "warnings": "Do not use if abdominal pain or vomiting is present."},
                    {"name": "Hydrocortisone Suppository / Cream", "dosage": "Apply or insert twice daily for up to 7 days.", "side_effects": "Burning, skin thinning.", "warnings": "Do not use continuously for more than 7 days."}
                ]
            },
            "Heart attack": {
                "description": "A medical emergency where the flow of blood to the heart muscle is abruptly blocked, usually by a blood clot, leading to tissue damage.",
                "causes": "Coronary artery disease, high cholesterol, hypertension, diabetes, smoking, or sudden plaque rupture.",
                "precautions": "seek immediate emergency help, chew an aspirin tablet, lie down quietly, monitor breathing",
                "specialist": "Cardiologist",
                "medicines": [
                    {"name": "Aspirin 325mg (Chewable)", "dosage": "Chew and swallow immediately at onset of chest pain.", "side_effects": "Heartburn, bleeding, nausea.", "warnings": "Seek emergency hospital care immediately; aspirin is only a first-aid support."},
                    {"name": "Clopidogrel 75mg", "dosage": "One tablet daily or as prescribed by emergency physician.", "side_effects": "Bruising, nosebleeds.", "warnings": "Only take under direct cardiological supervision."}
                ]
            },
            "Varicose veins": {
                "description": "Gnarled, enlarged veins, most commonly appearing in the legs and feet. For many, they are simply a cosmetic concern, but for others, they cause aching pain and discomfort.",
                "causes": "Weakened or damaged valves in the veins allowing blood to flow backward and pool.",
                "precautions": "wear compression stockings, elevate legs, avoid standing/sitting for long periods, exercise regularly",
                "specialist": "Vascular Surgeon",
                "medicines": [
                    {"name": "Diosmin + Hesperidin (500mg)", "dosage": "One tablet twice daily with meals.", "side_effects": "Nausea, diarrhea, headache.", "warnings": "Consult doctor if symptoms do not improve within 2 weeks."},
                    {"name": "Aescin (Horse Chestnut Extract)", "dosage": "One capsule daily.", "side_effects": "Stomach irritation (rare).", "warnings": "Avoid if having kidney insufficiency."}
                ]
            },
            "Hypothyroidism": {
                "description": "A condition in which the thyroid gland doesn't produce enough thyroid hormone, slowing down metabolism and causing fatigue, weight gain, and depression.",
                "causes": "Hashimoto's thyroiditis (autoimmune), iodine deficiency, radiation treatment, or surgical removal of the thyroid.",
                "precautions": "take levothyroxine on empty stomach, consume iodine-rich foods, monitor TSH levels annually",
                "specialist": "Endocrinologist",
                "medicines": [
                    {"name": "Levothyroxine Sodium 50mcg", "dosage": "One tablet daily in the morning on an empty stomach (30 mins before breakfast).", "side_effects": "Heart palpitations, nervousness, sweating (if dose too high).", "warnings": "Requires regular TSH level testing to adjust dose."},
                    {"name": "Selenium 200mcg", "dosage": "One tablet daily with food.", "side_effects": "Nail changes, garlic breath (if excess).", "warnings": "Supports thyroid hormone synthesis; check with endocrinologist."}
                ]
            },
            "Hyperthyroidism": {
                "description": "A condition where the thyroid gland produces too much thyroid hormone, accelerating the body's metabolism and causing weight loss, rapid heartbeat, and anxiety.",
                "causes": "Graves' disease (autoimmune), hyperfunctioning thyroid nodules, or thyroiditis.",
                "precautions": "avoid excess iodine, manage stress, monitor heart rate, take anti-thyroid medications",
                "specialist": "Endocrinologist",
                "medicines": [
                    {"name": "Methimazole 10mg", "dosage": "One tablet daily, adjusted based on thyroid hormone tests.", "side_effects": "Joint pain, skin rash, white blood cell count drop (rare).", "warnings": "Report any sudden fever or sore throat immediately."},
                    {"name": "Propranolol 40mg", "dosage": "One tablet 2-3 times daily (for heart rate control).", "side_effects": "Fatigue, cold extremities, sleep changes.", "warnings": "Do not stop taking suddenly."}
                ]
            },
            "Hypoglycemia": {
                "description": "A condition characterized by abnormally low blood glucose levels (usually below 70 mg/dL), causing shakiness, sweating, confusion, and dizziness.",
                "causes": "Excess insulin dosage, delayed meals, intense exercise without eating, or excessive alcohol intake.",
                "precautions": "carry candy/glucose tablets, consume 15g fast sugar immediately, eat a snack after recovery, check sugar",
                "specialist": "Endocrinologist",
                "medicines": [
                    {"name": "Dextrose (Glucose) Tablets", "dosage": "Chew 3 to 4 tablets (approx 15g glucose) immediately upon symptoms.", "side_effects": "Transient high blood sugar.", "warnings": "If unconscious, do not administer anything by mouth; seek emergency aid."},
                    {"name": "Glucagon Emergency Kit", "dosage": "1mg injection subcutaneously/intramuscularly (if patient unconscious).", "side_effects": "Nausea, vomiting.", "warnings": "Requires training for caregivers to administer."}
                ]
            },
            "Osteoarthristis": {
                "description": "The most common form of arthritis, occurring when the protective cartilage that cushions the ends of the bones wears down over time.",
                "causes": "Aging, joint injury, obesity, genetic factors, or chronic joint stress.",
                "precautions": "do low-impact exercise (swimming/cycling), maintain healthy weight, apply warm compresses, use knee braces",
                "specialist": "Rheumatologist / Orthopedist",
                "medicines": [
                    {"name": "Glucosamine + Chondroitin Sulfate", "dosage": "One tablet twice daily.", "side_effects": "Mild bloating, gas.", "warnings": "Takes 4-6 weeks to show potential benefits."},
                    {"name": "Ibuprofen 400mg", "dosage": "One tablet every 8 hours with food (use short-term).", "side_effects": "Stomach irritation, fluid retention.", "warnings": "Avoid if history of kidney disease or peptic ulcers."}
                ]
            },
            "Arthritis": {
                "description": "Inflammation of one or more joints, causing pain, stiffness, and reduced mobility. Common types include rheumatoid arthritis and osteoarthritis.",
                "causes": "Autoimmune response (Rheumatoid arthritis), cartilage wear and tear, or crystal deposition (gout).",
                "precautions": "avoid cold damp environments, do regular gentle stretches, apply warm therapy, reduce weight",
                "specialist": "Rheumatologist",
                "medicines": [
                    {"name": "Methotrexate 7.5mg", "dosage": "Once weekly as prescribed by rheumatologist.", "side_effects": "Nausea, mouth sores, liver changes.", "warnings": "Requires regular blood tests and folic acid supplementation. Absolute contraindication in pregnancy."},
                    {"name": "Naproxen 500mg", "dosage": "One tablet twice daily with food.", "side_effects": "Heartburn, abdominal pain.", "warnings": "Do not take on an empty stomach."}
                ]
            },
            "(vertigo) Paroxysmal Positional Vertigo": {
                "description": "Benign Paroxysmal Positional Vertigo (BPPV) is one of the most common causes of vertigo — the sudden sensation that you're spinning or that the inside of your head is spinning.",
                "causes": "Displacement of tiny calcium carbonate crystals in the inner ear canal, disrupting balance signals.",
                "precautions": "avoid sudden head movements, sleep with head slightly elevated, avoid bending down, sit down if dizzy",
                "specialist": "ENT Specialist / Neurologist",
                "medicines": [
                    {"name": "Betahistine 16mg", "dosage": "One tablet three times daily.", "side_effects": "Mild headache, indigestion.", "warnings": "Caution if history of asthma or peptic ulcers."},
                    {"name": "Meclizine 25mg", "dosage": "One tablet 1-2 times daily for acute vertigo.", "side_effects": "Drowsiness, dry mouth, tiredness.", "warnings": "May cause significant sedation; do not drive."}
                ]
            },
            "Acne": {
                "description": "A common skin condition that occurs when hair follicles become plugged with oil and dead skin cells, causing whiteheads, blackheads, or pimples.",
                "causes": "Excess oil production, clogged pores, bacteria (C. acnes), and hormonal activity.",
                "precautions": "wash face twice daily with gentle cleanser, avoid squeezing pimples, use non-comedogenic cosmetics, drink water",
                "specialist": "Dermatologist",
                "medicines": [
                    {"name": "Benzoyl Peroxide 5% Gel", "dosage": "Apply thin layer to affected areas once daily at night.", "side_effects": "Dryness, peeling, burning sensation.", "warnings": "May bleach clothing or hair. Use sunscreen during the day."},
                    {"name": "Doxycycline 100mg", "dosage": "One capsule daily with a large glass of water.", "side_effects": "Sun sensitivity, stomach upset.", "warnings": "Do not lie down for 30 minutes after taking to avoid esophageal irritation."}
                ]
            },
            "Urinary tract infection": {
                "description": "An infection in any part of your urinary system — kidneys, ureters, bladder, and urethra. Most infections involve the lower urinary tract.",
                "causes": "Bacteria (usually E. coli) entering the urinary tract through the urethra and multiplying in the bladder.",
                "precautions": "drink plenty of water, void bladder after intercourse, wipe front-to-back, avoid holding urine",
                "specialist": "Urologist / General Physician",
                "medicines": [
                    {"name": "Nitrofurantoin 100mg", "dosage": "One tablet twice daily for 5 days.", "side_effects": "Nausea, dark-colored urine (harmless), headache.", "warnings": "Take with food for best absorption."},
                    {"name": "Phenazopyridine 200mg", "dosage": "One tablet three times daily after meals (use max 2 days).", "side_effects": "Red/orange urine and tears (harmless), stomach upset.", "warnings": "Symptomatic pain relief only; does not cure the infection."}
                ]
            },
            "Psoriasis": {
                "description": "A skin disease that causes red, itchy scaly patches, most commonly on the knees, elbows, trunk, and scalp. It is a chronic autoimmune condition.",
                "causes": "Immune system problem causing skin cells to grow faster than normal, building up into thick patches.",
                "precautions": "moisturize skin regularly, avoid skin injuries, get moderate sun exposure, manage stress",
                "specialist": "Dermatologist",
                "medicines": [
                    {"name": "Clobetasol Propionate 0.05% Ointment", "dosage": "Apply sparingly to affected areas twice daily.", "side_effects": "Skin thinning, stretch marks.", "warnings": "Strong steroid; do not use continuously for more than 2 weeks without a break."},
                    {"name": "Coal Tar Topical Solution", "dosage": "Apply to scalp or skin as directed.", "side_effects": "Skin irritation, unpleasant odor.", "warnings": "Makes skin more sensitive to sunlight."}
                ]
            },
            "Impetigo": {
                "description": "A highly contagious skin infection that mainly affects infants and young children, appearing as red sores on the face, especially around the nose and mouth.",
                "causes": "Staphylococcus or Streptococcus bacteria entering through a small cut, scratch, or insect bite.",
                "precautions": "wash sores with warm soapy water, cover sores with bandages, isolate patient utensils and linen",
                "specialist": "Dermatologist / Pediatrician",
                "medicines": [
                    {"name": "Mupirocin 2% Ointment", "dosage": "Apply thin layer to affected sores 3 times daily for 5-10 days.", "side_effects": "Mild burning, stinging, pain.", "warnings": "For external use only; clean the crusts before applying."},
                    {"name": "Cephalexin 500mg", "dosage": "One tablet four times daily (for extensive infections).", "side_effects": "Nausea, diarrhea, skin rash.", "warnings": "Complete full course; report severe diarrhea."}
                ]
            }
        }

        # Clear existing data first
        Disease.objects.all().delete()
        Medicine.objects.all().delete()

        for name, data in diseases_data.items():
            disease = Disease.objects.create(
                name=name,
                description=data["description"],
                causes=data["causes"],
                precautions=data["precautions"],
                specialist=data["specialist"]
            )
            for med in data["medicines"]:
                Medicine.objects.create(
                    disease=disease,
                    medicine_name=med["name"],
                    dosage=med["dosage"],
                    side_effects=med["side_effects"],
                    warnings=med["warnings"]
                )

        self.stdout.write(self.style.SUCCESS("[+] Seeding completed successfully!"))
