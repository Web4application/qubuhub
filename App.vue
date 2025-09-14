<template>
  <div>
    <header>
      <h1>🚀 GPT-5 Mini Playground</h1>
    </header>
    <main>
      <section class="intro">
        <h2>Welcome!</h2>
        <p>Test the power of GPT-5 Mini with live features below.</p>
        <img src="assets/hero.jpg" alt="AI Illustration" class="hero" />
      </section>
      <section class="features">
        <div class="card" v-for="feature in features" :key="feature.title">
          <img :src="feature.icon" class="icon" />
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      features: [
        { title: 'Chat', desc: 'Converse with AI in real time.', icon: 'assets/chat.png' },
        { title: 'Text to Speech', desc: 'Convert AI responses to natural voice.', icon: 'assets/tts.png' },
        { title: 'Image Generation', desc: 'Generate unique visuals instantly.', icon: 'assets/image.png' },
        { title: 'Animation', desc: 'Bring ideas to life with motion.', icon: 'assets/anim.png' }
      ]
    }
  }
}
</script>

<style scoped>
main {
  padding: 2rem;
}
.intro {
  text-align: center;
  margin-bottom: 2rem;
}
.hero {
  width: 60%;
  margin: 1rem auto;
  display: block;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}
.card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.icon {
  width: 50px;
  margin-bottom: 0.5rem;
}
</style>
