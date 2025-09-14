<template>
  <div id="app">
    <header><h1>Fluukpe</h1></header>
    <main>
      <Auth v-if="!token" @authed="onAuthed" />
      <Dashboard v-else :token="token" />
    </main>
  </div>
</template>
<script>
import { ref } from 'vue'
import Auth from './components/Auth.vue'
import Dashboard from './components/Dashboard.vue'
export default { components:{Auth,Dashboard}, setup(){ const token=ref(localStorage.getItem('fp_token')||''); function onAuthed(t){ token.value=t; localStorage.setItem('fp_token',t)}; return {token,onAuthed}} }
</script>
