&lt;template&gt;
  &lt;div class="chat-page"&gt;
    &lt;div class="chat-page__sidebar"&gt;
      &lt;Sidebar /&gt;
    &lt;/div&gt;
    &lt;div class="chat-page__main"&gt;
      &lt;div class="chat-page__messages" ref="messagesContainer"&gt;
        &lt;ChatMessage
          v-for="message in messages"
          :key="message.id"
          :role="message.role"
          :content="message.content"
        /&gt;
      &lt;/div&gt;
      &lt;div class="chat-page__input"&gt;
        &lt;ChatInput @send="sendMessage" /&gt;
      &lt;/div&gt;
      &lt;div class="chat-page__tools"&gt;
        &lt;ToolPanel :tools="availableTools" @tool-select="handleToolSelect" /&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref, onMounted } from 'vue'
import ChatMessage from '@/components/ChatMessage.vue'
import ChatInput from '@/components/ChatInput.vue'
import Sidebar from '@/components/Sidebar.vue'
import ToolPanel from '@/components/ToolPanel.vue'

const messages = ref([])
const messagesContainer = ref(null)
const availableTools = ref([])

const sendMessage = async (content: string) => {
  // Add user message
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content
  })

  // TODO: Send to backend API
}

const handleToolSelect = (tool: string) => {
  // TODO: Handle tool selection
}

onMounted(() => {
  // TODO: Load conversation history and available tools
})
&lt;/script&gt;

&lt;style scoped&gt;
.chat-page {
  display: grid;
  grid-template-columns: 250px 1fr;
  height: 100vh;
}

.chat-page__main {
  display: grid;
  grid-template-rows: 1fr auto auto;
  gap: 1rem;
  padding: 1rem;
}

.chat-page__messages {
  overflow-y: auto;
}

.chat-page__tools {
  border-top: 1px solid #eee;
  padding-top: 1rem;
}
&lt;/style&gt;