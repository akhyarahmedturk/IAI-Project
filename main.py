# CLINIC EXPERT SYSTEM - Rule-Based Decision Support
# A simple expert system to help clinic staff decide patient referrals

# Knowledge Base - Symptom definitions and rules
def initialize_knowledge_base():
    """Initialize the knowledge base with symptom questions"""
    symptoms = {
        'fever': "Does the patient have a fever (temperature > 100.4°F)?",
        'high_fever': "Is the fever very high (temperature > 103°F)?",
        'cough': "Does the patient have a cough?",
        'severe_cough': "Is the cough severe or persistent?",
        'sore_throat': "Does the patient have a sore throat?",
        'runny_nose': "Does the patient have a runny or stuffy nose?",
        'sneezing': "Does the patient have sneezing?",
        'body_aches': "Does the patient have body aches or muscle pain?",
        'fatigue': "Does the patient experience unusual fatigue or weakness?",
        'difficulty_breathing': "Does the patient have difficulty breathing or shortness of breath?",
        'chest_pain': "Does the patient have chest pain?",
        'itchy_eyes': "Does the patient have itchy or watery eyes?",
        'headache': "Does the patient have a headache?",
        'nausea': "Does the patient have nausea or vomiting?",
        'duration_long': "Have symptoms lasted more than 10 days?"
    }
    return symptoms

def get_patient_symptoms():
    """Collect symptom information from user input"""
    print("\n" + "="*70)
    print("CLINIC EXPERT SYSTEM - PATIENT SYMPTOM ASSESSMENT")
    print("="*70)
    print("\nPlease answer the following questions with 'yes' or 'no'")
    print("-"*70)
    
    symptoms = initialize_knowledge_base()
    patient_data = {}
    
    for symptom_key, question in symptoms.items():
        while True:
            answer = input(f"\n{question} (yes/no): ").strip().lower()
            if answer in ['yes', 'y']:
                patient_data[symptom_key] = True
                break
            elif answer in ['no', 'n']:
                patient_data[symptom_key] = False
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    
    return patient_data

# Rule-Based Inference Engine
def apply_rules(symptoms):
    """
    Apply expert system rules to determine diagnosis and recommendation
    Returns: (diagnosis, recommendation, urgency_level, explanation)
    """
    
    # RULE 1: Emergency - Difficulty breathing or chest pain
    if symptoms['difficulty_breathing'] or symptoms['chest_pain']:
        return (
            "POTENTIAL EMERGENCY",
            "IMMEDIATE DOCTOR REFERRAL REQUIRED",
            "URGENT",
            "Difficulty breathing or chest pain requires immediate medical attention."
        )
    
    # RULE 2: Severe Flu - High fever with body aches and fatigue
    if symptoms['high_fever'] and symptoms['body_aches'] and symptoms['fatigue']:
        return (
            "Severe Influenza (Flu)",
            "REFER TO DOCTOR",
            "HIGH",
            "High fever with body aches and fatigue indicates severe flu requiring medical evaluation."
        )
    
    # RULE 3: Flu - Fever with cough and body aches
    if symptoms['fever'] and symptoms['cough'] and symptoms['body_aches']:
        return (
            "Influenza (Flu)",
            "REFER TO DOCTOR",
            "MODERATE",
            "Combination of fever, cough, and body aches is typical of flu."
        )
    
    # RULE 4: Severe Cold - Persistent symptoms
    if symptoms['duration_long'] and (symptoms['cough'] or symptoms['sore_throat']):
        return (
            "Prolonged Upper Respiratory Infection",
            "REFER TO DOCTOR",
            "MODERATE",
            "Symptoms lasting more than 10 days may indicate complications or secondary infection."
        )
    
    # RULE 5: Potential Allergy - Itchy eyes with sneezing and runny nose
    if symptoms['itchy_eyes'] and symptoms['sneezing'] and symptoms['runny_nose']:
        return (
            "Allergic Rhinitis (Allergy)",
            "HOME REMEDY RECOMMENDED",
            "LOW",
            "Itchy eyes with sneezing and runny nose are typical allergy symptoms. " +
            "Over-the-counter antihistamines may help. See doctor if symptoms persist."
        )
    
    # RULE 6: Allergy without eye symptoms
    if symptoms['sneezing'] and symptoms['runny_nose'] and not symptoms['fever']:
        return (
            "Possible Allergic Rhinitis",
            "HOME REMEDY RECOMMENDED",
            "LOW",
            "Sneezing and runny nose without fever suggests allergies. " +
            "Monitor symptoms and see doctor if worsening."
        )
    
    # RULE 7: Common Cold - Mild symptoms without fever
    if (symptoms['runny_nose'] or symptoms['sneezing']) and symptoms['sore_throat'] and not symptoms['fever']:
        return (
            "Common Cold",
            "HOME REMEDY RECOMMENDED",
            "LOW",
            "Typical cold symptoms. Rest, fluids, and over-the-counter medications recommended. " +
            "See doctor if symptoms worsen or persist beyond 7-10 days."
        )
    
    # RULE 8: Severe symptoms requiring evaluation
    if symptoms['severe_cough'] and (symptoms['fever'] or symptoms['difficulty_breathing']):
        return (
            "Severe Respiratory Infection",
            "REFER TO DOCTOR",
            "HIGH",
            "Severe cough with fever or breathing difficulty requires medical evaluation."
        )
    
    # RULE 9: Flu with digestive symptoms
    if symptoms['fever'] and symptoms['nausea'] and (symptoms['body_aches'] or symptoms['headache']):
        return (
            "Influenza with Gastrointestinal Symptoms",
            "REFER TO DOCTOR",
            "MODERATE",
            "Flu-like symptoms with nausea should be evaluated by a doctor."
        )
    
    # RULE 10: Mild cold symptoms
    if (symptoms['cough'] or symptoms['sore_throat'] or symptoms['runny_nose']) and not symptoms['fever']:
        return (
            "Mild Upper Respiratory Infection",
            "HOME REMEDY RECOMMENDED",
            "LOW",
            "Mild cold symptoms. Rest, stay hydrated, use over-the-counter medications. " +
            "See doctor if symptoms worsen or don't improve in 5-7 days."
        )
    
    # RULE 11: Fever alone - requires monitoring
    if symptoms['fever'] and not symptoms['high_fever']:
        return (
            "Fever - Unknown Source",
            "MONITOR AND CONSIDER DOCTOR VISIT",
            "MODERATE",
            "Fever without other clear symptoms. Monitor closely. " +
            "See doctor if fever persists beyond 3 days or worsens."
        )
    
    # RULE 12: High fever alone
    if symptoms['high_fever']:
        return (
            "High Fever",
            "REFER TO DOCTOR",
            "HIGH",
            "High fever requires medical evaluation to determine cause."
        )
    
    # Default rule - insufficient information
    return (
        "Insufficient Symptoms for Diagnosis",
        "MONITOR SYMPTOMS",
        "-",
        "No clear pattern detected.Please Enter symptoms."
    )

def display_recommendation(diagnosis, recommendation, urgency, explanation):
    """Display the expert system's recommendation in a formatted manner"""
    print("\n" + "="*70)
    print("EXPERT SYSTEM RECOMMENDATION")
    print("="*70)
    print(f"\nDiagnosis: {diagnosis}")
    print(f"Urgency Level: {urgency}")
    print(f"\nRecommendation: {recommendation}")
    print(f"\nExplanation: {explanation}")
    print("\n" + "="*70)
    
    # Additional advice based on urgency
    if urgency == "URGENT":
        print("\n⚠️  URGENT: Patient should see a doctor IMMEDIATELY or visit emergency room.")
    elif urgency == "HIGH":
        print("\n⚠️  HIGH PRIORITY: Schedule doctor appointment as soon as possible (same day if available).")
    elif urgency == "MODERATE":
        print("\nℹ️  MODERATE: Schedule doctor appointment within 1-2 days.")
    else:
        print("\nℹ️  LOW PRIORITY: Home care recommended. See doctor if symptoms worsen or persist.")
    
    print("="*70)

# Main program execution
def run_expert_system():
    """Main function to run the expert system"""
    print("\n" + "*"*70)
    print("*" + " "*68 + "*")
    print("*" + " "*15 + "CLINIC DECISION SUPPORT SYSTEM" + " "*23 + "*")
    print("*" + " "*68 + "*")
    print("*"*70)
    
    while True:
        # Collect patient symptoms
        patient_symptoms = get_patient_symptoms()
        
        # Apply expert rules
        diagnosis, recommendation, urgency, explanation = apply_rules(patient_symptoms)
        
        # Display results
        display_recommendation(diagnosis, recommendation, urgency, explanation)
        
        # Ask if user wants to assess another patient
        print("\n" + "-"*70)
        another = input("\nWould you like to assess another patient? (yes/no): ").strip().lower()
        if another not in ['yes', 'y']:
            print("\n" + "="*70)
            print("Thank you for using the Clinic Expert System!")
            print("="*70 + "\n")
            break

# Run the expert system
if __name__ == "__main__":
    run_expert_system()