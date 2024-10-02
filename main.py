import pandas as pd
data= pd.read_csv('dataset.csv')
print(data)

# Custom CSS for hover effect
st.markdown("""
<style>
.image-container img:hover {
    transform: scale(1.1);
    transition: 0.3s;
}
.image-container {
    display: flex;
    justify-content: space-around;
}
.movie-title {
    text-align: center;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)
