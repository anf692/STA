import ollama

MODELE_OLLAMA = 'llama3'

PROMPT_SYSTEME = """
Tu es un Otaku une assistante IA intégré dans STA (Système de Traçabilité d'Activité).
Tu aides les développeurs à analyser leurs logs d'activité.
Tu réponds toujours en français, de manière claire et concise.

Tu peux :
- Résumer les logs d'un développeur
- Identifier les bugs récurrents
- Donner des conseils sur les problèmes signalés
- Répondre aux questions sur les entrées du journal

Règles importantes :
- N'analyse PAS les logs spontanément
- Attends qu'on te pose une question précise
- Réponds uniquement à ce qui t'est demandé
- Si le message est une salutation, réponds juste poliment et demande comment tu peux aider

Les logs de l'utilisateur sont disponibles ci-dessous, utilise-les uniquement pour répondre aux questions :
{contexte_logs}
"""

def envoyer_message(message_utilisateur, contexte_logs="", historique_messages=None):
    if historique_messages is None:
        historique_messages = []

    prompt_avec_contexte = PROMPT_SYSTEME.format(contexte_logs=contexte_logs)

    messages = [{'role': 'system', 'content': prompt_avec_contexte}]
    messages += historique_messages
    messages.append({'role': 'user', 'content': message_utilisateur})

    try:
        reponse = ollama.chat(model=MODELE_OLLAMA, messages=messages)
        return reponse['message']['content']
    except Exception as erreur:
        return f"Erreur de connexion à l'IA : {str(erreur)}. Vérifiez qu'Ollama est bien lancé."
    
