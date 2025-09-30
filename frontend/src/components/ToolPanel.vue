&lt;template&gt;
  &lt;div class="tool-panel"&gt;
    &lt;div class="tool-panel__list"&gt;
      &lt;button
        v-for="tool in tools"
        :key="tool.id"
        :class="['tool-panel__tool', { active: selectedTool === tool.id }]"
        @click="selectTool(tool.id)"
      &gt;
        {{ tool.name }}
      &lt;/button&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref } from 'vue'

const props = defineProps<{
  tools: Array<{ id: string; name: string }>
}>()

const emit = defineEmits(['tool-select'])
const selectedTool = ref(null)

const selectTool = (toolId: string) => {
  selectedTool.value = toolId
  emit('tool-select', toolId)
}
&lt;/script&gt;

&lt;style scoped&gt;
.tool-panel {
  padding: 1rem 0;
}

.tool-panel__list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tool-panel__tool {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.tool-panel__tool:hover {
  background: #f5f5f5;
}

.tool-panel__tool.active {
  background: #0066cc;
  color: white;
  border-color: #0066cc;
}
&lt;/style&gt;