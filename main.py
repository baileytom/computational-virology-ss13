import itertools
import operator

class Symptom(object):
	def __init__(self, name, stealth, resistance, stage_speed, transmission, level):
		self.name = name
		self.stealth = stealth
		self.resistance = resistance
		self.stage_speed = stage_speed
		self.transmission = transmission
		self.level = level

class Disease(object):
	def __init__(self, symptoms):
		self.symptoms = symptoms
		self.stealth = sum(s.stealth for s in self.symptoms)
		self.resistance = sum(s.resistance for s in self.symptoms)
		self.stage_speed = sum(s.stage_speed for s in self.symptoms)
		self.transmission = sum(s.transmission for s in self.symptoms)

	def get_symptoms(self):
		return str.join(', ', list(map(lambda i: i.name, self.symptoms)))

symptoms = list(map(lambda i: Symptom(i[0], i[1], i[2], i[3], i[4], i[5]),
  [["Acute Respiratory Distress Syndrome",-2,0,-1,-2,7],
  ["Alopecia",0,1,2,2,4],
  ["Alkali perspiration",2,-2,-2,-2,7],
  ["Autophagocytosis Necrosis",-2,-2,1,-2,7],
  ["Choking",-3,-2,-2,-4,3],
  ["Coughing",-1,3,1,2,1],
  ["Confusion",1,-1,-3,0,4],
  ["Deafness",-1,-2,-1,-3,4],
  ["Deoxyribonucleic Acid Saboteur",-2,-3,0,-3,6],
  ["Dizziness",0,-2,-3,-1,4],
  ["Eternal Youth",3,4,4,-4,5],
  ["Facial Hypertrichosis",0,3,2,1,4],
  ["Fever",0,3,3,2,2],
  ["Hallucigen",-2,-3,-3,-1,5],
  ["Headache",-1,4,2,0,1],
  ["Inorganic Biology",-1,4,-2,3,5],
  ["Hyphema",-1,-4,-4,-3,5],
  ["Itching",0,3,3,1,1],
  ["Metabolic Boost",-1,-2,2,1,7],
  ["Mind Restoration",-1,-2,1,-3,5],
  ["Narcolepsy",-1,-2,-3,-4,6],
  ["Necrotic Metabolism",2,-2,1,0,5],
  ["Necrotizing Fasciitis",-3,-4,0,-4,6],
  ["Nocturnal Regeneration",2,-1,-2,-1,6],
  ["Plasma Fixation",0,3,-2,-2,8],
  ["Radioactive Resonance",-1,-2,0,-3,6],
  ["Regenerative Coma",0,-2,-3,-2,8],
  ["Revitiligo",-1,3,1,2,5],
  ["Self-Respiration",1,-3,-3,-4,6],
  ["Sensory Restoration",-1,-4,-4,-3,5],
  ["Shivering",0,2,2,2,2],
  ["Sneezing",-2,3,0,4,1],
  ["Spontaneous Combustion",1,-4,-4,-4,6],
  ["Starlight Condensation",-1,-2,0,1,6],
  ["Tissue Hydration",0,-1,0,-1,6],
  ["Toxolysis",0,-2,-2,-2,7],
  ["Viral Evolutionary Acceleration",-2,-3,5,3,3],
  ["Viral Self-Adaptation",3,5,-3,0,3],
  ["Vitiligo",2,0,3,1,5],
  ["Voice Change",-2,-3,-3,2,6],
  ["Vomiting",-2,-1,0,1,3],
  ["Weight Loss",-2,2,-2,-2,3]]))

print("Enter any required symptoms, or n to continue.")

required_symptoms = []
while True:
	selection = input()
	if selection == "n":
		break
	else:
		for s in symptoms:
			if s.name.lower() == selection.lower():
				if s not in required_symptoms:
					required_symptoms.append(s)

print("Enter the minimum stats for your disease:")
stealth_min = int(input("Stealth: "))
resistance_min = int(input("Resistance: "))
stage_speed_min = int(input("Stage speed: "))
transmission_min = int(input("Transmission: "))

max_symptom_level = int(input("Max symptom level: "))

airborne = input("Filter for airborne? y/n ").startswith("y")

sorting = input("Sorting? y/n ").startswith("y")
sort_key = None
if sorting:
	print("Enter the sorting order. 4 has most priority. ")
	stealth_sort = int(input("Stealth: "))
	resistance_sort = int(input("Resistance: "))
	stage_speed_sort = int(input("Stage speed: "))
	transmission_sort = int(input("Transmission: "))
	sort_dict = {
		stealth_sort: "stealth",
		resistance_sort: "resistance",
		stage_speed_sort: "stage_speed",
		transmission_sort: "transmission"
	}
	sort_key = operator.attrgetter(sort_dict[4], sort_dict[3], sort_dict[2], sort_dict[1])

# Custom key for spontaneous combustion
combustible_key = lambda x: x.stage_speed - x.stealth

matches = []
for length in range(1, 7):
	for i in itertools.combinations(filter(lambda i: i.level < max_symptom_level, symptoms),length-len(required_symptoms)):
		d = Disease(required_symptoms + list(i))
		transmission_level = d.transmission - len(d.symptoms)
		if airborne and transmission_level < 5:
			continue
		if sorting and (d.stealth < stealth_min or
			d.resistance < resistance_min or
			d.stage_speed < stage_speed_min or
			d.transmission < transmission_min):
			continue
		matches.append(d)

if sorting:
	matches.sort(key = sort_key)

for d in matches:
	print("__________________________________")
	print("Symptoms: {}".format(d.get_symptoms()))
	print("Stealth: {}".format(d.stealth))
	print("Resistance: {}".format(d.resistance))
	print("Stage speed: {}".format(d.stage_speed))
	print("Transmission: {}".format(d.transmission))
print("__________________________________")
