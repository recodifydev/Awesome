&lt;template&gt;
  &lt;nav class="sidebar"&gt;
    &lt;div class="sidebar__header"&gt;
      &lt;h1 class="sidebar__title"&gt;AI Agent&lt;/h1&gt;
    &lt;/div&gt;
    &lt;div class="sidebar__sessions"&gt;
      &lt;div
        v-for="session in sessions"
        :key="session.id"
        :class="['sidebar__session', { active: session.id === activeSessionId }]"
        @click="selectSession(session.id)"
      &gt;
        {{ session.name }}
      &lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="sidebar__actions"&gt;
      &lt;button @click="createNewSession" class="sidebar__new-btn"&gt;
        New Session
      &lt;/button&gt;
    &lt;/div&gt;
  &lt;/nav&gt;
&lt;/template&gt;

&lt;script setup lang="ts"&gt;
import { ref } from 'vue'

const sessions = ref([])
const activeSessionId = ref(null)

const selectSession = (id: string) => {
  activeSessionId.value = id
  // TODO: Load session
}

const createNewSession = async () => {
  // TODO: Create new session via API
}
&lt;/script&gt;

&lt;style scoped&gt;
.sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #f8f9fa;
  border-right: 1px solid #dee2e6;
}

.sidebar__header {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.sidebar__title {
  margin: 0;
  font-size: 1.25rem;
}

.sidebar__sessions {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.sidebar__session {
  padding: 0.75rem;
  margin: 0.25rem 0;
  border-radius: 4px;
  cursor: pointer;
}

.sidebar__session:hover {
  background: #e9ecef;
}

.sidebar__session.active {
  background: #0066cc;
  color: white;
}

.sidebar__actions {
  padding: 1rem;
  border-top: 1px solid #dee2e6;
}

.sidebar__new-btn {
  width: 100%;
  padding: 0.5rem;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.sidebar__new-btn:hover {
  background: #0052a3;
}
&lt;/style&gt;