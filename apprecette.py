import streamlit as st
import cloudscraper
from bs4 import BeautifulSoup
import time

# Configuration du style mobile
st.set_page_config(page_title="Marmiton List", page_icon="🛒")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)


def extraire_ingredients(url):
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    try:
        response = scraper.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Sélecteurs mis à jour
        items = soup.select('.recipe-ingredients__list__item') or \
                soup.select('.card-ingredient') or \
                soup.select('[class*="ingredient"]')

        res = []
        for item in items:
            t = " ".join(item.get_text(separator=' ').split()).strip()
            if t: res.append(t)
        return res
    except:
        return []


# --- INTERFACE ---
st.title("🍳 Marmiton Shopping")
st.write("Collez vos liens de recettes (un par ligne)")

# Zone de saisie adaptée au mobile
liens_bruts = st.text_area("Liens Marmiton :", height=150, placeholder="https://www.marmiton.org/...")

if st.button("Générer ma liste"):
    urls = [u.strip() for u in liens_bruts.split('\n') if u.strip()]

    if not urls:
        st.error("Ajoutez au moins un lien !")
    else:
        liste_complete = []
        barre_progression = st.progress(0)

        for i, url in enumerate(urls):
            # Mise à jour de la barre de progression
            barre_progression.progress((i + 1) / len(urls))
            ingredients = extraire_ingredients(url)
            liste_complete.extend(ingredients)
            time.sleep(0.5)  # Plus rapide mais sûr

        if liste_complete:
            st.success(f"✅ {len(urls)} recettes analysées")

            # Tri et affichage
            liste_complete.sort()

            st.markdown("### 🛒 Ma liste :")
            texte_final = "MA LISTE DE COURSES\n\n"

            for ing in liste_complete:
                st.checkbox(ing, key=ing + str(time.time()))  # Cases à cocher interactives
                texte_final += f"- {ing}\n"

            # Bouton de téléchargement
            st.download_button(
                label="💾 Enregistrer la liste (Fichier .txt)",
                data=texte_final,
                file_name="liste_courses.txt",
                mime="text/plain"
            )
        else:
            st.error("Aucun ingrédient trouvé. Vérifiez les liens.")