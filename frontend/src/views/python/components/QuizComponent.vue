<template>
	<!-- Present quiz questions and collect answers. -->
	<div class="container my-4">
		<h3 class="mb-4">Quiz</h3>

		<p v-if="isLoading">Loading quizzes...</p>
		<p v-else-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
		<p v-else-if="!hasQuizzes">No quizzes are available for this subtopic.</p>

		<form v-else @submit.prevent="submitQuiz">

			<div class="row">
				<section v-for="section in quizSections" 
					:key="section.key" 
					class="col-md-6 mb-4">
					<h4>{{ section.title }}</h4>
					<div v-for="(quiz, index) in section.items" 
						:key="quiz.id ?? `${section.key}-${index}`"
						class="card mb-3 p-3">
						<p><strong>{{ index + 1 }}. {{ quiz.question }}</strong></p>

						<template v-if="section.key === 'mcq'">
							<div v-for="option in quiz.options" :key="option" class="form-check">
								<input 
									:id="`${section.key}-${index}-${option}`" 
									v-model="responses[section.key][index]"
									class="form-check-input" 
									type="radio" 
									:name="`${section.key}-${index}`"
									:value="option" />
								<label class="form-check-label" :for="`${section.key}-${index}-${option}`">
									{{ option }}
								</label>
							</div>
						</template>

						<template v-else-if="section.key === 'true_false'">
							<div v-for="option in [true, false]" :key="String(option)" class="form-check">
								<input 
									:id="`${section.key}-${index}-${option}`" 
									v-model="responses[section.key][index]"
									class="form-check-input" 
									type="radio" 
									:name="`${section.key}-${index}`"
									:value="option" />
								<label class="form-check-label" :for="`${section.key}-${index}-${option}`">
									{{ option ? 'True' : 'False' }}
								</label>
							</div>
						</template>

						<input v-else v-model="responses[section.key][index]" class="form-control" type="text"
							placeholder="Enter answer" />
					</div>
				</section>
			</div>

			<div class="d-flex align-items-center flex-wrap gap-3 mt-3">
				<button class="btn btn-primary" type="submit" :disabled="isSubmitting">
					{{ isSubmitting ? 'Submitting...' : 'Submit Answers' }}
				</button>

				<div v-if="evaluation" class="alert alert-info mb-0 d-flex align-items-center" role="status">
					Submitted, your score: {{ evaluationMessage }} 
					<router-link 
						v-if="proceed" 
						class="btn btn-danger ms-auto" 
						:to="`/python/subtopic/${route.params.id}/code`">
						Continue to code
					</router-link>
					<span v-else class="text-danger"> &nbsp;&nbsp;(Minimum score required: 7/10)</span>
				</div>
			</div>
		</form>
	</div>


</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute } from "vue-router";
import { baseUrl } from "../../../config";

const proceed = ref(false);
const route = useRoute();
const quizzes = ref({});
const isLoading = ref(true);
const isSubmitting = ref(false);
const errorMessage = ref("");
const evaluation = ref(null);
const responses = reactive({ mcq: [], true_false: [] });

const quizSections = computed(() => [
	{ key: "mcq", title: "Multiple Choice", items: quizzes.value.mcq || [] },
	{ key: "true_false", title: "True / False", items: quizzes.value.true_false || [] },
]);

const hasQuizzes = computed(() => quizSections.value.some((section) => section.items.length));

const evaluationMessage = computed(() => {
	if (typeof evaluation.value === "string") return evaluation.value;
	return evaluation.value?.message || evaluation.value?.score + '/' + evaluation.value?.total || "Your answers were submitted.";
});

function normalizeQuizResponse(data) {
	if (Array.isArray(data)) return { mcq: data };
	return data.quizzes || data;
}

async function loadQuizzes() {
	// Load quiz questions for the current subtopic.
	try {
		const response = await fetch(`${baseUrl}/subtopics/${route.params.id}/quizzes`);
		if (!response.ok) throw new Error(`Request failed with status ${response.status}`);
		quizzes.value = normalizeQuizResponse(await response.json());
	} catch (error) {
		errorMessage.value = "Unable to load quizzes. Please try again.";
		console.error("Failed to load quizzes:", error);
	} finally {
		isLoading.value = false;
	}
}

async function submitQuiz() {
	// Submit answers and show the evaluation result.
	isSubmitting.value = true;
	errorMessage.value = "";
	evaluation.value = null;
	proceed.value = false;
	try {
		const response = await fetch(`${baseUrl}/subtopics/${route.params.id}/quizzes/evaluate/`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ answers: { ...responses } }),
		});
		if (!response.ok) throw new Error(`Request failed with status ${response.status}`);

		const result = await response.json();
		console.log("Result: ", result);
		
		evaluation.value = result;

		if (result.proceed) {						
			proceed.value = true;
		}
	} catch (error) {
		errorMessage.value = "Unable to submit your answers. Please try again.";
		console.error("Failed to evaluate quiz:", error);
	} finally {
		isSubmitting.value = false;
	}
}

onMounted(loadQuizzes);
</script>

<style scoped>
h3 {
	color: maroon;
}

.modal-dialog {
	max-width: 900px;
	width: min(90vw, 900px);
}

.container {
	max-height: 70vh;
	overflow-y: auto;
}
</style>
