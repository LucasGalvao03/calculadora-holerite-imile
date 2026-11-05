import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Calculadora de Holerite - iMile", page_icon="📦", layout="wide")

st.title("📦 Calculadora de Folha de Pagamento")
st.caption("Ajuste os parâmetros abaixo para calcular o salário líquido do mês.")

# Layout em duas colunas: Parâmetros (Esquerda) e Holerite (Direita)
col_input, col_result = st.columns([1, 1])

with col_input:
    st.subheader("⚙️ Configurações & Proventos")
    
    salario_base = st.number_input("Salário Base (R$)", value=0, step=50.0)
    horas_mensais = st.number_input("Base de Horas Mensais", value=220, step=10)
    
    col_dias1, col_dias2 = st.columns(2)
    with col_dias1:
        dias_uteis = st.number_input("Dias Úteis (Escala 6x1)", value=25, min_value=1)
    with col_dias2:
        domingos_feriados = st.number_input("Domingos e Feriados", value=5, min_value=0)
        
    st.divider()
    st.subheader("🌙 Adicionais e Variáveis")
    
    horas_extras_100 = st.number_input("Horas Extras 100% (horas)", value=0.0, step=0.5)
    horas_noturnas_relogio = st.number_input("Horas Noturnas Relógio (22h às 05h)", value=0.0, step=0.5)
    aplicar_hora_reduzida = st.checkbox("Aplicar Hora Noturna Reduzida CLT (52m30s)", value=True)

    st.divider()
    st.subheader("📉 Descontos Opcionais & Adiantamento")
    
    # Adiantamento fixo por padrão em R$ 1.025,00
    valor_adiantamento = st.number_input("Adiantamento / Quinzena (R$)", value=1025.0, step=25.0)
    desconto_vt = st.number_input("Desconto Vale Transportes (R$)", value=0.0, step=10.0)
    outros_descontos = st.number_input("Outros Descontos / Farmácia (R$)", value=0.0, step=10.0)

# --- CÁLCULOS ---
valor_hora = salario_base / horas_mensais if horas_mensais > 0 else 0.0

# Adicional Noturno (com ou sem redução CLT)
fator_reducao = (60 / 52.5) if aplicar_hora_reduzida else 1.0
horas_noturnas_computadas = horas_noturnas_relogio * fator_reducao

valor_he_100 = horas_extras_100 * (valor_hora * 2.0)
valor_ad_noturno = horas_noturnas_computadas * (valor_hora * 0.20)

# DSR sobre Variáveis
total_variaveis = valor_he_100 + valor_ad_noturno
valor_dsr = (total_variaveis / dias_uteis) * domingos_feriados if dias_uteis > 0 else 0.0

salario_bruto_total = salario_base + valor_he_100 + valor_ad_noturno + valor_dsr

# INSS Progressivo
def calcular_inss(bruto):
    if bruto <= 1412.00:
        return bruto * 0.075
    elif bruto <= 2666.68:
        return (bruto * 0.09) - 21.18
    elif bruto <= 4003.03:
        return (bruto * 0.12) - 101.18
    elif bruto <= 7786.02:
        return (bruto * 0.14) - 181.24
    else:
        return 908.85

inss = calcular_inss(salario_bruto_total)

# IRRF
def calcular_irrf(base):
    if base <= 2259.20:
        return 0.0
    elif base <= 2826.65:
        return (base * 0.075) - 169.44
    elif base <= 3751.05:
        return (base * 0.15) - 381.44
    elif base <= 4664.68:
        return (base * 0.225) - 662.77
    else:
        return (base * 0.275) - 896.00

base_irrf = salario_bruto_total - inss
irrf = max(calcular_irrf(base_irrf), 0.0)

# Totais
total_descontos = inss + irrf + valor_adiantamento + desconto_vt + outros_descontos
salario_liquido = salario_bruto_total - total_descontos

# --- EXIBIÇÃO DOS RESULTADOS ---
with col_result:
    st.subheader("📋 Demonstrativo de Pagamento")
    
    st.metric("Salário Líquido a Receber", f"R$ {salario_liquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.write("---")
    st.markdown("**PROVENTOS (Ganhos)**")
    st.write(f"- Salário Base: `R$ {salario_base:,.2f}`")
    if valor_he_100 > 0:
        st.write(f"- Horas Extras (100%): `R$ {valor_he_100:,.2f}`")
    if valor_ad_noturno > 0:
        st.write(f"- Adicional Noturno ({horas_noturnas_computadas:.2f}h CLT): `R$ {valor_ad_noturno:,.2f}`")
    if valor_dsr > 0:
        st.write(f"- DSR s/ Variáveis: `R$ {valor_dsr:,.2f}`")
    
    st.markdown(f"**Salário Bruto Total:** `R$ {salario_bruto_total:,.2f}`")
    
    st.write("---")
    st.markdown("**DESCONTOS**")
    st.write(f"- INSS: `R$ {inss:,.2f}`")
    if irrf > 0:
        st.write(f"- IRRF: `R$ {irrf:,.2f}`")
    if valor_adiantamento > 0:
        st.write(f"- Adiantamento (Dia 15): `R$ {valor_adiantamento:,.2f}`")
    if desconto_vt > 0:
        st.write(f"- Vale Transporte: `R$ {desconto_vt:,.2f}`")
    if outros_descontos > 0:
        st.write(f"- Outros Descontos: `R$ {outros_descontos:,.2f}`")
        
    st.markdown(f"**Total de Descontos:** `R$ {total_descontos:,.2f}`")
