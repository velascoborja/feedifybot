# Messages for the bot in different languages

MESSAGES = {
    "en": {
        # Start command
        "start_message": "Hi! Use /feed <ml> to log a bottle.\n\nYou can also set your timezone with /timezone <timezone> (e.g., /timezone Europe/Madrid)",
        
        # Feed command
        "feed_usage": "Usage: /feed <ml> (example: /feed 120)",
        "feed_invalid_number": "Value must be an integer. Example: /feed 120",
        "feed_logged": "Feed logged: {amount_ml} ml",
        "feed_error": "Sorry, there was an error logging your feed. Please try again.",
        
        # Timezone command
        "timezone_current": "Your current timezone is: {timezone}",
        "timezone_not_set": "You haven't set a timezone. Using default: Europe/Madrid\n\nTo set your timezone, use: /timezone <timezone>\nExample: /timezone America/New_York",
        "timezone_invalid": "Invalid timezone: {timezone}\n\nPlease use a valid timezone like:\n- Europe/Madrid\n- America/New_York\n- Asia/Tokyo\n- UTC",
        "timezone_set": "Timezone set to: {timezone}",
        "timezone_error": "Sorry, there was an error setting your timezone. Please try again.",
        
        # Daily summary
        "summary_with_feeds": "Today's summary:\nFeeds: {n_feeds}\nTotal: {total} ml",
        "summary_no_feeds": "You haven't logged any feeds today.",
    },
    
    "es": {
        # Start command
        "start_message": "¡Hola! Usa /feed <ml> para registrar un biberón.\n\nTambién puedes configurar tu zona horaria con /timezone <timezone> (ej: /timezone Europe/Madrid)",
        
        # Feed command
        "feed_usage": "Uso: /feed <ml> (ejemplo: /feed 120)",
        "feed_invalid_number": "El valor debe ser un número entero. Ejemplo: /feed 120",
        "feed_logged": "Alimentación registrada: {amount_ml} ml",
        "feed_error": "Lo siento, hubo un error al registrar tu alimentación. Por favor, inténtalo de nuevo.",
        
        # Timezone command
        "timezone_current": "Tu zona horaria actual es: {timezone}",
        "timezone_not_set": "No has configurado una zona horaria. Usando por defecto: Europe/Madrid\n\nPara configurar tu zona horaria, usa: /timezone <timezone>\nEjemplo: /timezone America/New_York",
        "timezone_invalid": "Zona horaria inválida: {timezone}\n\nPor favor usa una zona horaria válida como:\n- Europe/Madrid\n- America/New_York\n- Asia/Tokyo\n- UTC",
        "timezone_set": "Zona horaria configurada: {timezone}",
        "timezone_error": "Lo siento, hubo un error al configurar tu zona horaria. Por favor, inténtalo de nuevo.",
        
        # Daily summary
        "summary_with_feeds": "Resumen de hoy:\nTomas: {n_feeds}\nTotal: {total} ml",
        "summary_no_feeds": "Hoy no has registrado ninguna alimentación.",
    },
    
    "fr": {
        # Start command
        "start_message": "Salut! Utilisez /feed <ml> pour enregistrer un biberon.\n\nVous pouvez aussi définir votre fuseau horaire avec /timezone <timezone> (ex: /timezone Europe/Paris)",
        
        # Feed command
        "feed_usage": "Usage: /feed <ml> (exemple: /feed 120)",
        "feed_invalid_number": "La valeur doit être un nombre entier. Exemple: /feed 120",
        "feed_logged": "Alimentation enregistrée: {amount_ml} ml",
        "feed_error": "Désolé, il y a eu une erreur lors de l'enregistrement. Veuillez réessayer.",
        
        # Timezone command
        "timezone_current": "Votre fuseau horaire actuel est: {timezone}",
        "timezone_not_set": "Vous n'avez pas défini de fuseau horaire. Utilisation par défaut: Europe/Madrid\n\nPour définir votre fuseau horaire, utilisez: /timezone <timezone>\nExemple: /timezone America/New_York",
        "timezone_invalid": "Fuseau horaire invalide: {timezone}\n\nVeuillez utiliser un fuseau horaire valide comme:\n- Europe/Paris\n- America/New_York\n- Asia/Tokyo\n- UTC",
        "timezone_set": "Fuseau horaire défini: {timezone}",
        "timezone_error": "Désolé, il y a eu une erreur lors de la configuration du fuseau horaire. Veuillez réessayer.",
        
        # Daily summary
        "summary_with_feeds": "Résumé d'aujourd'hui:\nAlimentations: {n_feeds}\nTotal: {total} ml",
        "summary_no_feeds": "Vous n'avez enregistré aucune alimentation aujourd'hui.",
    },
    
    "it": {
        # Start command
        "start_message": "Ciao! Usa /feed <ml> per registrare un biberon.\n\nPuoi anche impostare il tuo fuso orario con /timezone <timezone> (es: /timezone Europe/Rome)",
        
        # Feed command
        "feed_usage": "Uso: /feed <ml> (esempio: /feed 120)",
        "feed_invalid_number": "Il valore deve essere un numero intero. Esempio: /feed 120",
        "feed_logged": "Alimentazione registrata: {amount_ml} ml",
        "feed_error": "Spiacente, c'è stato un errore nel registrare la tua alimentazione. Riprova.",
        
        # Timezone command
        "timezone_current": "Il tuo fuso orario attuale è: {timezone}",
        "timezone_not_set": "Non hai impostato un fuso orario. Uso predefinito: Europe/Madrid\n\nPer impostare il tuo fuso orario, usa: /timezone <timezone>\nEsempio: /timezone America/New_York",
        "timezone_invalid": "Fuso orario non valido: {timezone}\n\nUsa un fuso orario valido come:\n- Europe/Rome\n- America/New_York\n- Asia/Tokyo\n- UTC",
        "timezone_set": "Fuso orario impostato: {timezone}",
        "timezone_error": "Spiacente, c'è stato un errore nell'impostare il fuso orario. Riprova.",
        
        # Daily summary
        "summary_with_feeds": "Riepilogo di oggi:\nAlimentazioni: {n_feeds}\nTotale: {total} ml",
        "summary_no_feeds": "Non hai registrato nessuna alimentazione oggi.",
    }
}

def get_message(language_code: str, message_key: str, **kwargs):
    """
    Get a message in the specified language.
    Falls back to English if language or message not found.
    
    Args:
        language_code: Language code (e.g., 'es', 'en', 'fr', 'it')
        message_key: Key for the message
        **kwargs: Variables to format into the message
    
    Returns:
        Formatted message string
    """
    # Normalize language code (take only first 2 characters)
    lang = language_code.lower()[:2] if language_code else "en"
    
    # Fall back to English if language not supported
    if lang not in MESSAGES:
        lang = "en"
    
    # Get the message, fall back to English if key not found
    if message_key in MESSAGES[lang]:
        message = MESSAGES[lang][message_key]
    elif message_key in MESSAGES["en"]:
        message = MESSAGES["en"][message_key]
    else:
        return f"Message '{message_key}' not found"
    
    # Format the message with provided variables
    try:
        return message.format(**kwargs)
    except KeyError as e:
        # If formatting fails, return the unformatted message
        return message

def detect_user_language(update) -> str:
    """
    Detect user language from Telegram update.
    
    Args:
        update: Telegram Update object
        
    Returns:
        Language code (e.g., 'es', 'en', 'fr', 'it')
    """
    # Try to get language from user settings first
    if update.effective_user and update.effective_user.language_code:
        return update.effective_user.language_code
    
    # Fall back to English
    return "en"
