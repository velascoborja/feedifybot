# Messages for the bot in different languages

MESSAGES = {
    "en": {
        # Start command
        "start_message": "👋 Hi! Use /feed <ml> to log a bottle 🍼\n\n📊 Use /today to see today's summary\n⚙️ Use /setup to configure bot settings\n⏰ You can also set your timezone with /timezone <timezone> (e.g., /timezone Europe/Madrid)",
        
        # Feed command
        "feed_usage": "📝 Usage: /feed <ml> (example: /feed 120)",
        "feed_invalid_number": "❌ Value must be an integer. Example: /feed 120",
        "feed_logged": "✅ Feed logged: {amount_ml} ml 🍼",
        "feed_error": "😔 Sorry, there was an error logging your feed. Please try again.",
        
        # Timezone command
        "timezone_current": "🌍 Your current timezone is: {timezone}",
        "timezone_not_set": "⏰ You haven't set a timezone. Using default: Europe/Madrid\n\n🔧 To set your timezone, use: /timezone <timezone>\n📍 Example: /timezone America/New_York",
        "timezone_invalid": "❌ Invalid timezone: {timezone}\n\n✅ Please use a valid timezone like:\n🌍 Europe/Madrid\n🌎 America/New_York\n🌏 Asia/Tokyo\n🌐 UTC",
        "timezone_set": "✅ Timezone set to: {timezone} 🌍",
        "timezone_error": "😔 Sorry, there was an error setting your timezone. Please try again.",
        
        # Daily summary
        "summary_with_feeds": "📊 Today's summary:\n🍼 Feeds: {n_feeds}\n📏 Total: {total} ml",
        "summary_no_feeds": "📅 You haven't logged any feeds today. 🍼",
        
        # Today command
        "today_with_feeds": "📅 Today's feeding report:\n\n🍼 Total feeds: {n_feeds}\n📏 Total volume: {total} ml\n⏰ Average per feed: {average} ml\n\n⭐ Keep up the great work!",
        "today_no_feeds": "📅 Today's report:\n\n🍼 No feeds logged yet today.\n💡 Use /feed <ml> to log your first bottle!",
        
        # Setup command
        "setup_menu": "⚙️ Bot Setup\n\nChoose what you want to configure:",
        "setup_reminder_button": "⏰ Change daily reminder time",
        "setup_reminder_prompt": "⏰ What time would you like to receive your daily summary?\n\n📝 Please send the time in 24-hour format (HH:MM)\n📍 Examples: 21:00, 09:30, 18:15",
        "setup_reminder_invalid": "❌ Invalid time format. Please use HH:MM format (24-hour)\n📍 Examples: 21:00, 09:30, 18:15",
        "setup_reminder_set": "✅ Daily reminder set to: {time} 🕐\n\n📅 You'll receive your daily summary at this time every day!",
        "setup_reminder_current": "🕐 Your current daily reminder time is: {time}",
        "setup_reminder_error": "😔 Sorry, there was an error setting your reminder time. Please try again.",
    },
    
    "es": {
        # Start command
        "start_message": "👋 ¡Hola! Usa /feed <ml> para registrar un biberón 🍼\n\n📊 Usa /today para ver el resumen de hoy\n⚙️ Usa /setup para configurar el bot\n⏰ También puedes configurar tu zona horaria con /timezone <timezone> (ej: /timezone Europe/Madrid)",
        
        # Feed command
        "feed_usage": "📝 Uso: /feed <ml> (ejemplo: /feed 120)",
        "feed_invalid_number": "❌ El valor debe ser un número entero. Ejemplo: /feed 120",
        "feed_logged": "✅ Alimentación registrada: {amount_ml} ml 🍼",
        "feed_error": "😔 Lo siento, hubo un error al registrar tu alimentación. Por favor, inténtalo de nuevo.",
        
        # Timezone command
        "timezone_current": "🌍 Tu zona horaria actual es: {timezone}",
        "timezone_not_set": "⏰ No has configurado una zona horaria. Usando por defecto: Europe/Madrid\n\n🔧 Para configurar tu zona horaria, usa: /timezone <timezone>\n📍 Ejemplo: /timezone America/New_York",
        "timezone_invalid": "❌ Zona horaria inválida: {timezone}\n\n✅ Por favor usa una zona horaria válida como:\n🌍 Europe/Madrid\n🌎 America/New_York\n🌏 Asia/Tokyo\n🌐 UTC",
        "timezone_set": "✅ Zona horaria configurada: {timezone} 🌍",
        "timezone_error": "😔 Lo siento, hubo un error al configurar tu zona horaria. Por favor, inténtalo de nuevo.",
        
        # Daily summary
        "summary_with_feeds": "📊 Resumen de hoy:\n🍼 Tomas: {n_feeds}\n📏 Total: {total} ml",
        "summary_no_feeds": "📅 Hoy no has registrado ninguna alimentación. 🍼",
        
        # Today command
        "today_with_feeds": "📅 Reporte de alimentación de hoy:\n\n🍼 Total de tomas: {n_feeds}\n📏 Volumen total: {total} ml\n⏰ Promedio por toma: {average} ml\n\n⭐ ¡Sigue así de bien!",
        "today_no_feeds": "📅 Reporte de hoy:\n\n🍼 Aún no has registrado tomas hoy.\n💡 ¡Usa /feed <ml> para registrar tu primer biberón!",
        
        # Setup command
        "setup_menu": "⚙️ Configuración del Bot\n\nElige qué quieres configurar:",
        "setup_reminder_button": "⏰ Cambiar hora del recordatorio diario",
        "setup_reminder_prompt": "⏰ ¿A qué hora quieres recibir tu resumen diario?\n\n📝 Por favor envía la hora en formato 24 horas (HH:MM)\n📍 Ejemplos: 21:00, 09:30, 18:15",
        "setup_reminder_invalid": "❌ Formato de hora inválido. Por favor usa el formato HH:MM (24 horas)\n📍 Ejemplos: 21:00, 09:30, 18:15",
        "setup_reminder_set": "✅ Recordatorio diario configurado a las: {time} 🕐\n\n📅 ¡Recibirás tu resumen diario a esta hora todos los días!",
        "setup_reminder_current": "🕐 Tu hora actual del recordatorio diario es: {time}",
        "setup_reminder_error": "😔 Lo siento, hubo un error al configurar tu hora de recordatorio. Por favor, inténtalo de nuevo.",
    },
    
    "fr": {
        # Start command
        "start_message": "👋 Salut! Utilisez /feed <ml> pour enregistrer un biberon 🍼\n\n📊 Utilisez /today pour voir le résumé d'aujourd'hui\n⚙️ Utilisez /setup pour configurer le bot\n⏰ Vous pouvez aussi définir votre fuseau horaire avec /timezone <timezone> (ex: /timezone Europe/Paris)",
        
        # Feed command
        "feed_usage": "📝 Usage: /feed <ml> (exemple: /feed 120)",
        "feed_invalid_number": "❌ La valeur doit être un nombre entier. Exemple: /feed 120",
        "feed_logged": "✅ Alimentation enregistrée: {amount_ml} ml 🍼",
        "feed_error": "😔 Désolé, il y a eu une erreur lors de l'enregistrement. Veuillez réessayer.",
        
        # Timezone command
        "timezone_current": "🌍 Votre fuseau horaire actuel est: {timezone}",
        "timezone_not_set": "⏰ Vous n'avez pas défini de fuseau horaire. Utilisation par défaut: Europe/Madrid\n\n🔧 Pour définir votre fuseau horaire, utilisez: /timezone <timezone>\n📍 Exemple: /timezone America/New_York",
        "timezone_invalid": "❌ Fuseau horaire invalide: {timezone}\n\n✅ Veuillez utiliser un fuseau horaire valide comme:\n🌍 Europe/Paris\n🌎 America/New_York\n🌏 Asia/Tokyo\n🌐 UTC",
        "timezone_set": "✅ Fuseau horaire défini: {timezone} 🌍",
        "timezone_error": "😔 Désolé, il y a eu une erreur lors de la configuration du fuseau horaire. Veuillez réessayer.",
        
        # Daily summary
        "summary_with_feeds": "📊 Résumé d'aujourd'hui:\n🍼 Alimentations: {n_feeds}\n📏 Total: {total} ml",
        "summary_no_feeds": "📅 Vous n'avez enregistré aucune alimentation aujourd'hui. 🍼",
        
        # Today command
        "today_with_feeds": "📅 Rapport d'alimentation d'aujourd'hui:\n\n🍼 Total d'alimentations: {n_feeds}\n📏 Volume total: {total} ml\n⏰ Moyenne par alimentation: {average} ml\n\n⭐ Continuez comme ça!",
        "today_no_feeds": "📅 Rapport d'aujourd'hui:\n\n🍼 Aucune alimentation enregistrée aujourd'hui.\n💡 Utilisez /feed <ml> pour enregistrer votre premier biberon!",
        
        # Setup command
        "setup_menu": "⚙️ Configuration du Bot\n\nChoisissez ce que vous voulez configurer:",
        "setup_reminder_button": "⏰ Changer l'heure du rappel quotidien",
        "setup_reminder_prompt": "⏰ À quelle heure souhaitez-vous recevoir votre résumé quotidien?\n\n📝 Veuillez envoyer l'heure au format 24 heures (HH:MM)\n📍 Exemples: 21:00, 09:30, 18:15",
        "setup_reminder_invalid": "❌ Format d'heure invalide. Veuillez utiliser le format HH:MM (24 heures)\n📍 Exemples: 21:00, 09:30, 18:15",
        "setup_reminder_set": "✅ Rappel quotidien configuré à: {time} 🕐\n\n📅 Vous recevrez votre résumé quotidien à cette heure chaque jour!",
        "setup_reminder_current": "🕐 Votre heure actuelle de rappel quotidien est: {time}",
        "setup_reminder_error": "😔 Désolé, il y a eu une erreur lors de la configuration de votre heure de rappel. Veuillez réessayer.",
    },
    
    "it": {
        # Start command
        "start_message": "👋 Ciao! Usa /feed <ml> per registrare un biberon 🍼\n\n📊 Usa /today per vedere il riassunto di oggi\n⚙️ Usa /setup per configurare il bot\n⏰ Puoi anche impostare il tuo fuso orario con /timezone <timezone> (es: /timezone Europe/Rome)",
        
        # Feed command
        "feed_usage": "📝 Uso: /feed <ml> (esempio: /feed 120)",
        "feed_invalid_number": "❌ Il valore deve essere un numero intero. Esempio: /feed 120",
        "feed_logged": "✅ Alimentazione registrata: {amount_ml} ml 🍼",
        "feed_error": "😔 Spiacente, c'è stato un errore nel registrare la tua alimentazione. Riprova.",
        
        # Timezone command
        "timezone_current": "🌍 Il tuo fuso orario attuale è: {timezone}",
        "timezone_not_set": "⏰ Non hai impostato un fuso orario. Uso predefinito: Europe/Madrid\n\n🔧 Per impostare il tuo fuso orario, usa: /timezone <timezone>\n📍 Esempio: /timezone America/New_York",
        "timezone_invalid": "❌ Fuso orario non valido: {timezone}\n\n✅ Usa un fuso orario valido come:\n🌍 Europe/Rome\n🌎 America/New_York\n🌏 Asia/Tokyo\n🌐 UTC",
        "timezone_set": "✅ Fuso orario impostato: {timezone} 🌍",
        "timezone_error": "😔 Spiacente, c'è stato un errore nell'impostare il fuso orario. Riprova.",
        
        # Daily summary
        "summary_with_feeds": "📊 Riepilogo di oggi:\n🍼 Alimentazioni: {n_feeds}\n📏 Totale: {total} ml",
        "summary_no_feeds": "📅 Non hai registrato nessuna alimentazione oggi. 🍼",
        
        # Today command
        "today_with_feeds": "📅 Rapporto alimentazione di oggi:\n\n🍼 Totale alimentazioni: {n_feeds}\n📏 Volume totale: {total} ml\n⏰ Media per alimentazione: {average} ml\n\n⭐ Continua così!",
        "today_no_feeds": "📅 Rapporto di oggi:\n\n🍼 Nessuna alimentazione registrata oggi.\n💡 Usa /feed <ml> per registrare il tuo primo biberon!",
        
        # Setup command
        "setup_menu": "⚙️ Configurazione Bot\n\nScegli cosa vuoi configurare:",
        "setup_reminder_button": "⏰ Cambia orario promemoria giornaliero",
        "setup_reminder_prompt": "⏰ A che ora vuoi ricevere il tuo riassunto giornaliero?\n\n📝 Per favore invia l'ora in formato 24 ore (HH:MM)\n📍 Esempi: 21:00, 09:30, 18:15",
        "setup_reminder_invalid": "❌ Formato ora non valido. Per favore usa il formato HH:MM (24 ore)\n📍 Esempi: 21:00, 09:30, 18:15",
        "setup_reminder_set": "✅ Promemoria giornaliero impostato alle: {time} 🕐\n\n📅 Riceverai il tuo riassunto giornaliero a quest'ora ogni giorno!",
        "setup_reminder_current": "🕐 Il tuo orario attuale del promemoria giornaliero è: {time}",
        "setup_reminder_error": "😔 Spiacente, c'è stato un errore nell'impostare il tuo orario di promemoria. Riprova.",
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
