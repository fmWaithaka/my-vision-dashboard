<template>
  <div class="bg-white p-6 rounded-lg shadow-md mb-8">
    <h2 class="text-2xl font-semibold mb-4 text-gray-800">Vision Assistant Chat</h2>

    <div class="h-64 overflow-y-auto border border-gray-300 rounded-lg p-4 mb-4 bg-gray-50">
      <div v-for="(message, index) in messages" :key="index" :class="message.sender === 'user' ? 'text-right' : 'text-left'">
        <span :class="message.sender === 'user' ? 'bg-blue-500 text-white rounded-lg px-3 py-1 inline-block my-1' : 'bg-gray-200 text-gray-800 rounded-lg px-3 py-1 inline-block my-1'">
          {{ message.text }}
        </span>
      </div>
    </div>

    <div class="flex">
      <input
        type="text"
        v-model="userMessage"
        @keyup.enter="sendMessage"
        placeholder="Ask your vision assistant..."
        class="flex-grow border border-gray-300 rounded-l-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        :disabled="isLoading"
      />
      <button
        @click="sendMessage"
        :disabled="!userMessage.trim() || isLoading"
        class="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ isLoading ? 'Sending...' : 'Send' }}
      </button>
    </div>
    <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LLMChat',
  data() {
    return {
      userMessage: '',
      messages: [],
      isLoading: false,
      error: null,
      apiBaseUrl: 'http://127.0.0.1:8000/api/',
      conversationId: null, // <-- NEW: To store the current conversation ID
    };
  },
  methods: {
    async sendMessage() {
      if (!this.userMessage.trim()) {
        return;
      }

      this.error = null;
      this.isLoading = true;
      const messageToSend = this.userMessage;
      this.messages.push({ sender: 'user', text: messageToSend });
      this.userMessage = '';

      try {
        // Prepare the payload, conditionally including conversation_id
        const payload = {
          message: messageToSend,
        };
        if (this.conversationId) {
          payload.conversation_id = this.conversationId;
        }

        const response = await axios.post(`${this.apiBaseUrl}llm-chat/`, payload); // <-- Changed: sending payload

        const aiResponse = response.data.response || "Sorry, I couldn't get a clear response.";
        this.messages.push({ sender: 'ai', text: aiResponse });

        // <-- NEW: Store the conversation ID from the response
        if (response.data.conversation_id) {
          this.conversationId = response.data.conversation_id;
        }

      } catch (err) {
        console.error('Error sending message to LLM:', err);
        this.error = 'Failed to get response from assistant. Please try again.';
        if (err.response && err.response.data && err.response.data.error) {
            this.error = `Error: ${err.response.data.error}`;
        }
        this.messages.pop(); // Remove user message if not sent or failed
      } finally {
        this.isLoading = false;
        this.$nextTick(() => {
          const chatDisplay = this.$el.querySelector('.overflow-y-auto');
          if (chatDisplay) { // Added a check here, just in case
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
          }
        });
      }
    },
  },
  mounted() {
    // Optionally, you could try to load a saved conversationId from localStorage here
    // If you want to persist conversations across browser sessions.
    // e.g., this.conversationId = localStorage.getItem('lastConversationId');
    this.messages.push({ sender: 'ai', text: "Hello! How can I help you with your vision today?" });
  }
};
</script>