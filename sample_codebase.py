
def is_valid_email(address):
    """Check whether a string looks like a valid email address."""
    import re
    return bool(re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", address))

def format_currency(amount, currency="USD"):
    """Format a number as a currency string, e.g. 1234.5 -> "$1,234.50"."""
    symbol = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3"}.get(currency, "")
    return f"{symbol}{amount:,.2f}"

def calculate_discount(price, percent_off):
    """Return the price after applying a percentage discount."""
    return round(price * (1 - percent_off / 100), 2)

def slugify(text):
    """Turn a title into a URL-friendly slug, e.g. "Hello World!" -> "hello-world"."""
    import re
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def is_palindrome(text):
    """Check whether a string reads the same forwards and backwards, ignoring case and spaces."""
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]
