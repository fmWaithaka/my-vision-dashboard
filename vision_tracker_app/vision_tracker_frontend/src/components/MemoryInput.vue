<template>
  <div class="bg-white p-6 rounded-lg shadow-md mb-8">
    <h2 class="text-2xl font-semibold mb-4 text-gray-800">Add a New Memory / Reflection</h2>
    <p class="text-sm text-gray-600 mb-4">Jot down your thoughts, reflections, learnings, or anything relevant to your vision. These memories will help your Vision Assistant understand you better over time.</p>

    <div class="mb-4">
      <label for="memoryContent" class="block text-sm font-medium text-gray-700 sr-only">Memory Content</label>
      <textarea
        id="memoryContent"
        v-model="memoryText"
        rows="4"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-400 focus:border-blue-400 sm:text-sm resize-y"
        placeholder="Write down a new memory, a key learning, or a reflection... (e.g., 'Today I read a book on Stoicism and reflected on emotional resilience.')"
        :disabled="isLoading"
      ></textarea>
    </div>

    <button
      @click="saveMemory"
      :disabled="!memoryText.trim() || isLoading"
      class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <span v-if="isLoading">Saving...</span>
      <span v-else>Save Memory</span>
    </button>

    <p v-if="successMessage" class="mt-3 text-sm text-green-600">{{ successMessage }}</p>
    <p v-if="errorMessage" class="mt-3 text-sm text-red-600">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MemoryInput',
  data() {
    return {
      memoryText: '',
      isLoading: false,
      successMessage: '',
      errorMessage: '',
      apiBaseUrl: 'http://127.0.0.1:8000/api/', // Base URL for your Django API
    };
  },
  methods: {
    async saveMemory() {
      if (!this.memoryText.trim()) {
        this.errorMessage = 'Memory content cannot be empty.';
        return;
      }

      this.isLoading = true;
      this.successMessage = '';
      this.errorMessage = '';

      try {
        const response = await axios.post(`${this.apiBaseUrl}memories/`, {
          text_content: this.memoryText,
          // metadata: {} // Can send empty object or omit if 'default=dict' is set in Django model
          // category: null // If you link to a category, you can send category ID here
        });

        console.log('Memory saved successfully:', response.data);
        this.successMessage = 'Memory saved successfully! Your assistant just got smarter.';
        this.memoryText = ''; // Clear the input field
      } catch (error) {
        console.error('Error saving memory:', error.response ? error.response.data : error.message);
        this.errorMessage = 'Failed to save memory. Please try again.';
        if (error.response && error.response.data) {
            this.errorMessage += ` Error: ${JSON.stringify(error.response.data)}`;
        }
      } finally {
        this.isLoading = false;
        // Clear messages after a few seconds
        setTimeout(() => {
            this.successMessage = '';
            this.errorMessage = '';
        }, 5000);
      }
    },
  },
};
</script>

<style scoped>
/* No specific styles needed if Tailwind is sufficient */
</style>