<template>
  <div id="app" class="main-container">
    <div class="header">
      <h1 class="app-title">Stock Sense</h1>
      <p class="quote">An AI-Powered Stock Trend Prediction System</p>
      <p class="warning-text">WARNING: THIS IS NOT FINANCIAL ADVICE</p>
    </div>
    <div class="body">
      <div class="input-section">
        <input v-model="stockSymbol" class="input-field" placeholder="Enter stock symbol" />
        <input v-model="startDate" class="input-field" type="date" />
        <input v-model="endDate" class="input-field" type="date" />
        <button @click="predict" class="predict-button">Predict</button>
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
      <div v-if="combinedPlotImage" class="plot-section">
        <h2 class="plot-title">Actual vs Predicted Stock Prices</h2>
        <img :src="combinedPlotImage" alt="Actual vs Predicted Stock Prices" class="plot-image" />
      </div>
      <p v-if="mse" class="mse-message">Mean Squared Error (MSE): {{ mse }}</p>
      <div v-if="prediction" class="prediction-section">
        <h2 class="prediction-title">OUR PREDICTION</h2>
        <h1 class="pred" :style="{ color: predictionColor }">
          <span v-if="prediction === 'up'" class="prediction-green">{{ prediction.toUpperCase() }}</span>
          <span v-else-if="prediction === 'down'" class="prediction-red">{{ prediction.toUpperCase() }}</span>
          <span v-else>{{ prediction }}</span>
          <p v-if="accuracy" class="accuracy-message">Accuracy: {{ accuracy }}%</p>
        </h1>
        <p v-if="prediction === 'down'" class="scroll-hint">To see why scroll down</p>
        <div v-if="prediction === 'down'" class="scroll-down-arrow" @click="scrollToBottom">
          <span class="arrow">↓</span>
        </div>
      </div>
  </div>


  <div class="graphs">
    <div class="holder">
      <div class="first_graph" v-if="historicalPlotImage">
            <h2>Historical Stock Prices</h2>
            <img :src="historicalPlotImage" alt="Historical Stock Prices" />
          </div>
          <div class="second_graph" v-if="predictedPlotImage">
            <h2>Predicted Stock Prices</h2>
            <img :src="predictedPlotImage" alt="Predicted Stock Prices" />
          </div>
    </div>


        </div>
    </div>




</template>


<script>
import axios from 'axios';


export default {
  data() {
    return {
      stockSymbol: '',
      startDate: '',
      endDate: '',
      prediction: null,
      error: null,
      combinedPlotImage: null,
      mse: null,
      historicalPlotImage: null,
      predictedPlotImage: null,
      accuracy: null,
    };
  },
  computed: {
    predictionColor() {
      if (this.prediction === 'up') {
        return 'green';
      } else if (this.prediction === 'down') {
        return 'red';
      }
      return 'inherit';
    },
  },
  methods: {
    async predict() {
      this.error = null;
      this.combinedPlotImage = null;
      this.mse = null;


      if (!this.stockSymbol.trim() || !this.startDate || !this.endDate) {
        this.error = "Please enter a stock symbol, start date, and end date.";
        return;
      }


      try {
        const response = await axios.post('http://127.0.0.1:5000/predict', {
          stock: this.stockSymbol,
          start_date: this.startDate,
          end_date: this.endDate,
         
        });


        this.prediction = response.data.prediction;
        this.mse = response.data.mse;
        if (response.data.historical_plot_image && response.data.predicted_plot_image) {
          this.historicalPlotImage = `data:image/png;base64,${response.data.historical_plot_image}`;
          this.predictedPlotImage = `data:image/png;base64,${response.data.predicted_plot_image}`;
        }
      } catch (err) {
        this.error = "An error occurred while fetching the prediction.";
      }
    },
    scrollToBottom() {
      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
      });
    },
  },
};
</script>


<style>
:root {
  background-color: black;
}


#app {
  background-color: black;
  color: white;
  font-family: Trebuchet MS, sans-serif;
  text-align: center;
  padding: 1.5em;
}


.main-container {
  margin: 0 auto;
  max-width: 52em;
  align-items:center;
}


.header {
  margin-bottom: 1.5em;
}


.app-title {
  font-size: 3.25em;
  margin-bottom: 0.20em;
}


.graphs {
  width: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: nowrap; /* Prevent wrapping to multiple lines */
}


.holder {
  max-width: 100%;
  flex: 1;
  overflow: hidden;
}


.first_graph,
.second_graph {
  max-width: 100%;
  flex: 1;
  overflow: hidden;
}


.first_graph img,
.second_graph img {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
  margin: 0 auto; /* Center the image horizontally within its container */
}




.quote {
  font-size: 1.25em;
  margin-top: -0.25em;
  margin-bottom: 2em;
  color: #ADB0B3;
}


.warning-text {
  font-size: 1.25em;
  color: red;
  font-weight: bold;
  margin-top: 0.5em;
}


.body {
  margin: 0 auto;
}


.input-section {
  margin-bottom: 1.5em;
}


.input-field {
  font-family: Trebuchet MS, sans-serif;
  padding: 0.75em;
  margin: 0.75em;
}


.predict-button {
  padding: 0.75em 1.5em;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}


.predict-button:hover {
  background-color: #0056b3;
}


.error-message {
  color: red;
  margin-top: 1.5em;
}


.prediction-section {
  text-align: center;
  margin-top: 1.5em;
}


.prediction-title {
  font-size: 1.5em;
  margin-bottom: 0.5em;
}


.pred {
  font-size: 2em;
  margin-top: 0;
}


.prediction-green {
  color: green;
}


.prediction-red {
  color: red;
}


.plot-section {
  margin: 1.5em 0;
}


.plot-title {
  margin: 0.75em 0;
}


.plot-image {
  max-width: 100%;
  height: auto;
  margin: 0.75em 0;
}


.mse-message {
  margin-top: 1.5em;
}
</style>

