&lt;template&gt;
  &lt;div :class="['chat-message', role]"&gt;
    &lt;div class="chat-message__content"&gt;
      &lt;div class="chat-message__role"&gt;{{ role }}&lt;/div&gt;
      &lt;div class="chat-message__text"&gt;
        &lt;component :is="markdownRenderer" :source="content" /&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps<{
  role: 'user' | 'assistant'
  content: string
}>()

const markdownRenderer = computed(() => ({
  render() {
    return marked(props.content)
  }
}))
&lt;/script&gt;

&lt;style scoped&gt;
.chat-message {
  display: flex;
  padding: 1rem;
  margin: 0.5rem 0;
}

.chat-message__content {
  max-width: 80%;
}

.chat-message__role {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #666;
}

.chat-message__text {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
}

.chat-message.assistant .chat-message__text {
  background: #e3f2fd;
}

.chat-message.user {
  justify-content: flex-end;
}

.chat-message.user .chat-message__text {
  background: #f0f4c3;
}
&lt;/style&gt;