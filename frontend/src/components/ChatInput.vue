&lt;template&gt;
  &lt;div class="chat-input"&gt;
    &lt;textarea
      v-model="message"
      @keyup.enter.exact.prevent="sendMessage"
      placeholder="Type your message..."
      class="chat-input__textarea"
    /&gt;
    &lt;button @click="sendMessage" class="chat-input__button"&gt;Send&lt;/button&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref } from 'vue'

const message = ref('')
const emit = defineEmits(['send'])

const sendMessage = () => {
  if (message.value.trim()) {
    emit('send', message.value)
    message.value = ''
  }
}
&lt;/script&gt;

&lt;style scoped&gt;
.chat-input {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-top: 1px solid #eee;
}

.chat-input__textarea {
  flex: 1;
  min-height: 40px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}

.chat-input__button {
  padding: 0.5rem 1rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-input__button:hover {
  background: #0052a3;
}
&lt;/style&gt;