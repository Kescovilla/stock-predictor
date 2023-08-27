<template>
  <div id="app">
    <h1>Stock Price Trend Predictor</h1>
    <input v-model="stockSymbol" placeholder="Enter stock symbol" />
    <input v-model="startDate" type="date" />
    <input v-model="endDate" type="date" />
    <button @click="predict">Predict</button>
    <p v-if="error">{{ error }}</p>
    <h1 class="pred" v-if="prediction">prediction: {{ prediction }}</h1>
    <div v-if="historicalPlotImage">
      <h2>Historical Stock Prices</h2>
      <img :src="historicalPlotImage" alt="Historical Stock Prices" />
    </div>
    <div v-if="predictedPlotImage">
      <h2>Predicted Stock Prices</h2>
      <img :src="predictedPlotImage" alt="Predicted Stock Prices" />
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
      historicalPlotImage: null,
      predictedPlotImage: null,
    };
  },
  methods: {
    async predict() {
      this.error = null;
      this.historicalPlotImage = null;
      this.predictedPlotImage = null; // Clear previous data

      if (!this.stockSymbol.trim()) {
        this.error = "Please enter a stock symbol.";
        return;
      }

      if (!this.startDate || !this.endDate) {
        this.error = "Please select both start date and end date.";
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:5000/predict', {
          stock: this.stockSymbol,
          start_date: this.startDate,
          end_date: this.endDate,
        });

        this.prediction = response.data.prediction;
        if (response.data.historical_plot_image && response.data.predicted_plot_image) {
          this.historicalPlotImage = `data:image/png;base64,${response.data.historical_plot_image}`;
          this.predictedPlotImage = `data:image/png;base64,${response.data.predicted_plot_image}`;
        }
      } catch (err) {
        this.error = "An error occurred while fetching the prediction.";
      }
    },
  },
};
</script>

<style>
</style>
