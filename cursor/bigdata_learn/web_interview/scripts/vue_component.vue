<template>
  <div class="user-profile">
    <div class="avatar">
      <img :src="user.avatar" :alt="user.name" />
    </div>
    <div class="info">
      <h2>{{ displayName }}</h2>
      <p>{{ user.email }}</p>
      <p>年龄：{{ user.age }}</p>
      <p>部门：{{ user.department }}</p>
    </div>
    <div class="actions">
      <button @click="handleEdit">编辑</button>
      <button @click="handleDelete">删除</button>
    </div>
    <slot name="footer"></slot>
  </div>
</template>

<script>
export default {
  name: 'UserProfile',
  props: {
    user: {
      type: Object,
      required: true,
      validator(value) {
        return value && value.name && value.email;
      }
    }
  },
  data() {
    return {
      isEditing: false
    };
  },
  computed: {
    displayName() {
      return this.user.name.toUpperCase();
    }
  },
  watch: {
    'user.name'(newVal, oldVal) {
      console.log(`Name changed from ${oldVal} to ${newVal}`);
    }
  },
  methods: {
    handleEdit() {
      this.isEditing = true;
      this.$emit('edit', this.user);
    },
    handleDelete() {
      if (confirm('确定要删除吗？')) {
        this.$emit('delete', this.user.id);
      }
    }
  },
  beforeCreate() {
    console.log('beforeCreate');
  },
  created() {
    console.log('created');
  },
  beforeMount() {
    console.log('beforeMount');
  },
  mounted() {
    console.log('mounted');
  },
  beforeUpdate() {
    console.log('beforeUpdate');
  },
  updated() {
    console.log('updated');
  },
  beforeUnmount() {
    console.log('beforeUnmount');
  },
  unmounted() {
    console.log('unmounted');
  }
};
</script>

<style scoped>
.user-profile {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.info h2 {
  margin: 0 0 10px 0;
  color: #333;
}

.info p {
  margin: 5px 0;
  color: #666;
}

.actions {
  display: flex;
  gap: 10px;
}

.actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
}

.actions button:hover {
  background-color: #0056b3;
}
</style>
