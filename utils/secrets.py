import os

from dotenv import load_dotenv


def load_dotenv_and_streamlit_secrets():
    """Load local .env values and override with Streamlit secrets when available."""
    load_dotenv()

    try:
        import streamlit as st

        # If Streamlit is running and secrets are configured, mirror them into os.environ.
        # This allows downstream libraries that only read environment variables to work.
        if hasattr(st, "secrets"):
            for key, value in st.secrets.items():
                if value is None:
                    continue
                if isinstance(value, (dict, list)):
                    continue
                if key not in os.environ or os.environ.get(key) == "":
                    os.environ[key] = str(value)
    except Exception:
        pass


def get_secret(name, default=None):
    """Return a secret from Streamlit secrets first, then fallback to os.environ."""
    try:
        import streamlit as st

        if hasattr(st, "secrets") and name in st.secrets:
            value = st.secrets[name]
            if value is not None:
                return value
    except Exception:
        pass

    return os.environ.get(name, default)
