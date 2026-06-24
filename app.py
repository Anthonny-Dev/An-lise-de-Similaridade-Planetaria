import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import ProjetoPlanetas as pp

st.set_page_config(
    page_title="Exoplanet Explorer",
    page_icon="🌍",
    layout="wide"
)


st.markdown("""
<style>

.stApp{
    background-color:#070a12;
    color:#f0e6c8;
}

section[data-testid="stSidebar"]{
    background:#0d1220;
}

h1,h2,h3{
    color:#f0e6c8 !important;
}

.main-title{
    text-align:center;
    font-size:3rem;
    font-weight:bold;
    color:#f0e6c8;
}

.main-title span{
    color:#4fa3e0;
}

.subtitle{
    text-align:center;
    color:#a0a0a0;
    margin-bottom:30px;
}

.winner-card{
    background:linear-gradient(
        135deg,
        rgba(79,163,224,0.15),
        rgba(13,18,32,0.95)
    );
    border:1px solid rgba(79,163,224,.4);
    border-radius:18px;
    padding:25px;
    margin-bottom:25px;
}

div[data-testid="metric-container"]{
    background:#111827;
    border:1px solid rgba(79,163,224,.25);
    padding:15px;
    border-radius:12px;
}

div[data-testid="stDataFrame"]{
    border:1px solid rgba(79,163,224,.25);
    border-radius:12px;
}

.block-container{
    padding-top:2rem;
}

div[data-testid="stImage"]{
    display: flex;
    justify-content: center;
    align-items: center;
    justify-items: center;    
}
            
</style>
""", unsafe_allow_html=True)


import ProjetoPlanetas as pp



st.markdown(
    """
    <div class="main-title">
        EXPLORADOR DE <span>EXOPLANETAS</span>
    </div>

    <div class="subtitle">
        Sistema de Busca por Exoplanetas Semelhantes à Terra
    </div>
    """,
    unsafe_allow_html=True
)



col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total de Planetas",
        len(pp.df)
    )

with col2:
    st.metric(
        "≤ 200 anos-luz",
        len(pp.filtro1_distancia)
    )

with col3:
    st.metric(
        "Raio Similar",
        len(pp.filtro4_raio)
    )

with col4:
    st.metric(
        "Planetas Perfeitos",
        len(pp.planetas_perfeitos)
    )

st.divider()


vencedor = pp.gemeo_estrutural.iloc[0]

if not pp.planetas_perfeitos.empty:
    vencedor = pp.planetas_perfeitos.iloc[0]
else:
    vencedor = pp.gemeo_estrutural.iloc[0]

nome_vencedor = vencedor["pl_name"]
densidade_vencedor = vencedor["pl_dens"]
raio_vencedor = vencedor["pl_rade"]

img_vencedor = 'Teegardens_Star_b.jpg'

st.markdown(
    f"""
    <div class="winner-card">

    <h2>
    🏆 Melhor Candidato Encontrado
    </h2>

    <h1 style="color:#4fa3e0;">
    {nome_vencedor}
    <br>
    </h1>
    <p>
    Planeta com menor distância estrutural em relação à Terra
    considerando todos os filtros da análise.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)
st.image(img_vencedor, width=920)


col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"Raio da Terra",
        f"{pp.RAIO_DA_TERRA} R⊕"
    )
    
    st.metric(
        f"Densidade da Terra",
        f"{pp.DENSIDADE_DA_TERRA} g/cm³"
    )

with col2:
    st.metric(
        f"Raio do {nome_vencedor}",
        f"{raio_vencedor:.2f} R⊕"
    )
    st.metric(
        f"Densidade do {nome_vencedor}",
        f"{densidade_vencedor:.2f} g/cm³"
    )

st.divider()

# ==========================
# GRÁFICO PRINCIPAL
# ==========================

st.subheader("🌎 Raio × Densidade")

fig, ax = plt.subplots(figsize=(10,6))

ax.scatter(
    pp.df_filtrado["pl_rade"],
    pp.df_filtrado["pl_dens"],
    alpha=0.5,
    color="lightgray",
    label="Exoplanetas"
)

ax.scatter(
    raio_vencedor,
    densidade_vencedor,
    color="red",
    s=150,
    edgecolor="black",
    label=nome_vencedor
)

ax.scatter(
    1.0,
    5.51,
    color="blue",
    marker="X",
    s=150,
    edgecolor="black",
    label="Terra"
)

ax.set_title("Onde está a nossa Nova Terra?")
ax.set_xlabel("Raio (Raios Terrestres)")
ax.set_ylabel("Densidade (g/cm³)")
ax.legend()
ax.grid(alpha=0.2)

st.pyplot(fig, use_container_width=True)

st.divider()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("Filtros")

distancia_maxima = st.sidebar.slider(
    "Distância máxima (anos-luz)",
    min_value=10,
    max_value=200,
    value=200
)

planetas_proximos = pp.df[
    pp.df["distancia_anos_luz"] <= distancia_maxima
]

st.sidebar.metric(
    "Planetas encontrados",
    len(planetas_proximos)
)

# ==========================
# TABELA PRINCIPAL
# ==========================

st.subheader("📡 Catálogo de Planetas Potencialmente Habitáveis")

if not pp.planetas_perfeitos.empty:

    tabela = pp.planetas_perfeitos[
        [
            "pl_name",
            "distancia_anos_luz",
            "pl_bmasse",
            "pl_rade",
            "pl_insol",
            "pl_dens"
        ]
    ].copy()

    tabela.columns = [
        "Planeta",
        "Distância (anos-luz)",
        "Massa",
        "Raio",
        "Radiação",
        "Densidade"
    ]

    st.dataframe(
        tabela,
        use_container_width=True,
        height=400
    )

else:

    st.warning(
        "Nenhum planeta passou simultaneamente por todos os filtros."
    )

# ==========================
# ANÁLISES INDIVIDUAIS
# ==========================

st.divider()

st.subheader("🔬 Resultados dos Filtros")

with st.expander("Filtro 1 — Distância"):
    st.dataframe(
        pp.filtro1_distancia[
            ["pl_name", "distancia_anos_luz"]
        ],
        use_container_width=True
    )

with st.expander("Filtro 2 — Gravidade"):
    st.dataframe(
        pp.planetas_gravidade_similar[
            ["pl_name", "st_logg"]
        ],
        use_container_width=True
    )

with st.expander("Filtro 3 — Massa"):
    st.dataframe(
        pp.filtro3_massa[
            ["pl_name", "pl_bmasse"]
        ],
        use_container_width=True
    )

with st.expander("Filtro 4 — Raio"):
    st.dataframe(
        pp.filtro4_raio[
            ["pl_name", "pl_rade"]
        ],
        use_container_width=True
    )

with st.expander("Filtro 5 — Radiação"):
    st.dataframe(
        pp.filtro5_radiacao[
            ["pl_name", "pl_insol"]
        ],
        use_container_width=True
    )

with st.expander("Filtro Magnético"):
    st.dataframe(
        pp.filtro_magnetico_real[
            ["pl_name", "pl_dens", "pl_rade"]
        ],
        use_container_width=True
    )

# ==========================
# RODAPÉ
# ==========================

st.divider()

st.caption(
    "Projeto Nova Terra • Busca de Exoplanetas com características semelhantes à Terra"
)