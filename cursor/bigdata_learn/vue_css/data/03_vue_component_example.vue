<template>
  <div class="user-card">
    <div class="avatar">
      <img :src="user.avatar" :alt="user.name" />
    </div>
    <div class="info">
      <h3>{{ user.name }}</h3>
      <p class="email">{{ user.email }}</p>
      <p class="role">{{ user.role }}</p>
    </div>
    <button class="btn-primary" @click="handleClick">查看详情</button>
  </div>
</template>

<script>
export default {
  name: 'UserCard',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  methods: {
    handleClick() {
      this.$emit('view-detail', this.user.id)
    }
  }
}
</script>

<style scoped>
.user-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.avatar img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.info {
  flex: 1;
}

.info h3 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.email {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0.25rem 0;
}

.role {
  color: #3498db;
  font-size: 0.85rem;
  margin: 0.25rem 0;
}

.btn-primary {
  padding: 0.5rem 1rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #2980b9;
}
</style>
