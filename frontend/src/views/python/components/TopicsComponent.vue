<template>
    <div class="container my-2 p-2">
        
        <div class="topics-grid">
            <div v-for="topic in topics" :key="topic.id">
            <div class="card me-4" style="width: 18rem; height: 22rem;">
                <router-link 
                    class="topic-link" 
                    :to="{ name: 'topic-summary', params: { id: topic.id } }">
                    <img
                    :src="require('../../../assets/' + topic.img_name)"
                    class="card-img-top"
                    :alt="topic.img_name"
                    />
                    <div class="card-body">
                        <p class="card-text">{{ topic.title }}</p>
                    </div>
                </router-link>
            </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { baseUrl } from "../../../config";

const topics = ref([]);

onMounted(async () => {
    try {
        const response = await fetch(`${baseUrl}/topics/`);

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        topics.value = await response.json();
    } catch (error) {
        console.error("Failed to load topics:", error);
    }
});
</script>

<style scoped>
.theory-container {
    padding: 24px;
}

h3 {
    margin: 0 0 16px;
    /* font-size: 1.5rem; */
    color: maroon;
    /* text-align: center; */
}

.theory-iframe {
    width: 100%;
    min-height: 800px;
    border: 1px solid #dfe3e8;
    border-radius: 10px;
    background: #fff;
}

.topic-link {
    font-size: 1.25rem;
}

.topics-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}
</style>