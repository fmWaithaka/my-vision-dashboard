<template>
  <div class="bg-amber-50 text-stone-800 min-h-screen flex flex-col items-center py-8 px-4">
    <div class="container mx-auto max-w-4xl bg-white shadow-xl rounded-lg p-6 md:p-10">

      <header class="text-center mb-8 md:mb-12">
        <h1 class="text-3xl md:text-4xl font-bold text-teal-700">My Personal Vision</h1>
        <p class="text-stone-600 mt-2 text-sm md:text-base">An interactive exploration of my guiding principles and aspirations.</p>
      </header>

      <section id="fullVision" class="mb-10 p-6 bg-amber-100 rounded-lg shadow">
        <h2 class="text-xl md:text-2xl font-semibold text-teal-600 mb-4 text-center">My Guiding Statement</h2>
        <p class="text-lg md::text-xl leading-relaxed text-stone-700 text-center">
          "I am a <span class="vision-phrase font-semibold text-teal-700" data-target="leadershipGrowth">good leader</span>,
          <span class="vision-phrase font-semibold text-teal-700" data-target="leadershipGrowth">continuously refreshing my skills</span> and
          <span class="vision-phrase font-semibold text-teal-700" data-target="leadershipGrowth">expanding my network with inspiring individuals</span>.
          Grounded in <span class="vision-phrase font-semibold text-teal-700" data-target="foundationalPrinciples">spiritual and emotional maturity</span>,
          I make <span class="vision-phrase font-semibold text-teal-700" data-target="foundationalPrinciples">wise decisions</span>,
          foster <span class="vision-phrase font-semibold text-teal-700" data-target="foundationalPrinciples">dignity</span>, and
          communicate with <span class="vision-phrase font-semibold text-teal-700" data-target="foundationalPrinciples">articulate grace</span>.
          As a <span class="vision-phrase font-semibold text-teal-700" data-target="rolesActions">devoted husband and father</span>,
          a <span class="vision-phrase font-semibold text-teal-700" data-target="rolesActions">creative problem-solver</span>, and
          a <span class="vision-phrase font-semibold text-teal-700" data-target="rolesActions">champion for accessible innovation</span>,
          I leave a <span class="vision-phrase font-semibold text-teal-700" data-target="ultimateImpact">profound and positive mark</span> on
          <span class="vision-phrase font-semibold text-teal-700" data-target="ultimateImpact">every life I touch</span> and
          <span class="vision-phrase font-semibold text-teal-700" data-target="ultimateImpact">every challenge I undertake</span>."
        </p>
      </section>

      <section id="visionChartSection" class="mb-10 content-section">
        <h2 class="text-xl md:text-2xl font-semibold text-teal-600 mb-6 text-center">Vision Focus Areas</h2>
        <p class="text-center text-stone-600 mb-6 text-sm md:text-base">This chart conceptually illustrates a balanced commitment across the core areas of my vision. It serves as a reminder of the holistic nature of my aspirations.</p>
        <div class="chart-container bg-stone-50 p-4 rounded-lg shadow">
          <canvas id="visionBalanceChart"></canvas>
        </div>
      </section>

      <div class="space-y-10">
        <section id="leadershipGrowth" class="p-6 rounded-lg shadow-md bg-stone-50 content-section">
          <h3 class="text-xl font-semibold text-teal-600 mb-3 flex items-center"><span class="text-2xl mr-2">🌱</span>Leadership & Continuous Growth</h3>
          <p class="text-stone-700 leading-relaxed text-sm md:text-base">This area of my vision focuses on my development as an effective and inspiring leader. It involves a commitment to lifelong learning, consistently updating my skill set to remain relevant and impactful. Equally important is cultivating a strong, supportive network of individuals who challenge and inspire me, fostering mutual growth and collaboration. Key aspects include:</p>
          <ul class="list-disc list-inside mt-2 text-stone-600 space-y-1 text-sm md:text-base">
            <li>Developing strong leadership qualities.</li>
            <li>Actively seeking new knowledge and skills.</li>
            <li>Building and nurturing a network of inspiring peers and mentors.</li>
            <li>Adapting to new challenges with a growth mindset.</li>
          </ul>
        </section>

        <section id="foundationalPrinciples" class="p-6 rounded-lg shadow-md bg-stone-50 content-section">
          <h3 class="text-xl font-semibold text-teal-600 mb-3 flex items-center"><span class="text-2xl mr-2">🧭</span>Foundational Principles</h3>
          <p class="text-stone-700 leading-relaxed text-sm md:text-base">My vision is anchored by core principles that guide my actions and decisions. Spiritual and emotional maturity provide the bedrock for wisdom and sound judgment. Fostering dignity in all interactions is paramount, ensuring respect for myself and others. Effective communication, characterized by articulate grace, allows me to convey ideas clearly and build strong relationships. This includes:</p>
          <ul class="list-disc list-inside mt-2 text-stone-600 space-y-1 text-sm md:text-base">
            <li>Cultivating spiritual and emotional well-being.</li>
            <li>Making decisions based on wisdom and ethical considerations.</li>
            <li>Treating everyone with dignity and respect.</li>
            <li>Communicating clearly, thoughtfully, and respectfully.</li>
          </ul>
        </section>

        <section id="rolesActions" class="p-6 rounded-lg shadow-md bg-stone-50 content-section">
          <h3 class="text-xl font-semibold text-teal-600 mb-3 flex items-center"><span class="2xl mr-2">🤝</span>Key Roles & Actions</h3>
          <p class="text-stone-700 leading-relaxed text-sm md:text-base">This part of my vision defines how I manifest my principles and growth in tangible ways. Being a devoted husband and father is a central role, focused on nurturing and supporting my family. Professionally and personally, I aim to be a creative problem-solver, finding innovative solutions to challenges. I am passionate about championing accessible innovation, striving to make solutions available to those who need them most. I am passionate about championing accessible innovation, striving to make solutions available to those who need them most. My actions are driven by:</p>
          <ul class="list-disc list-inside mt-2 text-stone-600 space-y-1 text-sm md:text-base">
            <li>Prioritizing family and fulfilling my roles as a husband and father.</li>
            <li>Approaching problems with creativity and a solution-oriented mindset.</li>
            <li>Advocating for and developing innovations that are accessible to all.</li>
            <li>Taking initiative and being proactive in my endeavors.</li>
          </ul>
        </section>

        <section id="ultimateImpact" class="p-6 rounded-lg shadow-md bg-stone-50 content-section">
          <h3 class="text-xl font-semibold text-teal-600 mb-3 flex items-center"><span class="text-2xl mr-2">🌟</span>Ultimate Impact & Legacy</h3>
          <p class="text-stone-700 leading-relaxed text-sm md:text-base">The culmination of my vision is the lasting positive impact I aim to create. This isn't just about grand achievements, but about the positive influence I have on every individual I interact with and every challenge I face. It's about leaving a legacy of positive change, thoughtful solutions, and inspiring others through my actions and character. My goal is to ensure that:</p>
          <ul class="list-disc list-inside mt-2 text-stone-600 space-y-1 text-sm md:text-base">
            <li>My actions contribute positively to the lives of others.</li>
            <li>I approach challenges as opportunities for positive impact.</li>
            <li>My contributions are meaningful and enduring.</li>
            <li>I inspire others through my journey and how I make them feel.</li>
          </ul>
        </section>
      </div>

      <MemoryInput class="mt-10" />

      <div class="mt-8 mb-6 p-4 bg-teal-50 rounded-lg shadow-inner">
        <h3 class="text-lg font-semibold text-teal-700 mb-4">Update Focus Values (API Test)</h3>
        <div v-for="category in visionData" :key="category.id" class="flex items-center justify-between mb-3 last:mb-0">
          <label :for="'focus-input-' + category.id" class="block text-sm font-medium text-stone-700 w-1/2 md:w-auto">{{ category.name }}:</label>
          <input
            :id="'focus-input-' + category.id"
            type="number"
            v-model.number="category.focus_value"
            @change="updateCategoryFocus(category)"
            class="mt-1 block w-20 md:w-24 px-3 py-2 border border-stone-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm text-center"
            min="0"
            max="100"
          />
          <span class="text-stone-600 ml-2">%</span>
        </div>
        <p class="text-center text-xs text-stone-500 mt-4">Changes save automatically on input change.</p>
      </div>
      <div class="chart-container bg-stone-50 p-4 rounded-lg shadow">
        <canvas id="visionBalanceChart"></canvas>
      </div>

      <LLMChat class="mt-10" />

      <footer class="text-center mt-12 pt-6 border-t border-stone-300">
        <p class="text-sm text-stone-500">&copy; <span id="currentYear"></span> My Personal Vision Dashboard. Crafted with purpose.</p>
      </footer>

    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import Chart from 'chart.js/auto';
import LLMChat from '@/components/LLMChat.vue';
import MemoryInput from '@/components/MemoryInput.vue'; 

// Reactive variable to hold the fetched vision data
const visionData = ref([]);
let visionChartInstance = null; // To store the Chart.js instance for updates

const updateCategoryFocus = async (category) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/vision-data/${category.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(category)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`HTTP error! status: ${response.status}, message: ${JSON.stringify(errorData)}`);
    }

    console.log(`Category ${category.name} updated successfully! New value: ${category.focus_value}`);
    updateChart();
  } catch (error) {
    console.error("Error updating vision data:", error);
  }
};

const fetchVisionData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/vision-data/');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    visionData.value = data;
    console.log("Fetched vision data:", visionData.value);
    updateChart();
  } catch (error) {
    console.error("Error fetching vision data:", error);
  }
};

const updateChart = () => {
  const ctx = document.getElementById('visionBalanceChart')?.getContext('2d');
  if (!ctx) {
    console.error("Failed to get context for visionBalanceChart");
    return;
  }

  if (visionChartInstance) {
    visionChartInstance.destroy();
  }

  const labels = visionData.value.map(item => item.name);
  const dataValues = visionData.value.map(item => item.focus_value);

  visionChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Commitment Focus',
        data: dataValues,
        backgroundColor: [
          'rgba(20, 184, 166, 0.6)',
          'rgba(13, 148, 136, 0.6)',
          'rgba(15, 118, 110, 0.6)',
          'rgba(17, 94, 89, 0.6)'
        ],
        borderColor: [
          'rgba(20, 184, 166, 1)',
          'rgba(13, 148, 136, 1)',
          'rgba(15, 118, 110, 1)',
          'rgba(17, 94, 89, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          beginAtZero: true,
          max: 120,
          grid: {
            color: 'rgba(120, 113, 108, 0.1)'
          },
          ticks: {
            color: '#57534e'
          }
        },
        y: {
          grid: {
            display: false
          },
          ticks: {
            color: '#57534e',
            font: {
              size: 10
            },
            callback: function(value, index, values) {
              const label = this.getLabelForValue(value);
              if (label.length > 16) {
                const words = label.split(' ');
                let lines = [''];
                let currentLine = 0;
                words.forEach(word => {
                  if ((lines[currentLine] + word).length > 16 && lines[currentLine] !== '') {
                    currentLine++;
                    lines[currentLine] = '';
                  }
                  lines[currentLine] += word + ' ';
                });
                return lines.map(line => line.trim());
              }
              return label;
            }
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          enabled: true,
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          titleFont: { size: 14 },
          bodyFont: { size: 12 },
          callbacks: {
            label: function(context) {
              return ` Focus Area: ${context.dataset.data[context.dataIndex]}% Commitment`;
            }
          }
        }
      }
    }
  });
};


onMounted(() => {
  document.getElementById('currentYear').textContent = new Date().getFullYear();
  fetchVisionData();

  const phrases = document.querySelectorAll('.vision-phrase');
  const sections = {
    leadershipGrowth: document.getElementById('leadershipGrowth'),
    foundationalPrinciples: document.getElementById('foundationalPrinciples'),
    rolesActions: document.getElementById('rolesActions'),
    ultimateImpact: document.getElementById('ultimateImpact')
  };

  let lastHighlightedSection = null;

  phrases.forEach(phrase => {
    phrase.addEventListener('click', function () {
      const targetId = this.getAttribute('data-target');
      const targetSection = sections[targetId];

      if (targetSection) {
        if (lastHighlightedSection && lastHighlightedSection !== targetSection) {
          lastHighlightedSection.classList.remove('section-highlight', 'bg-teal-50');
        }
        targetSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        targetSection.classList.add('section-highlight', 'bg-teal-50');
        lastHighlightedSection = targetSection;
        setTimeout(() => {
          if (targetSection.classList.contains('section-highlight')) {
            targetSection.classList.remove('section-highlight', 'bg-teal-50');
          }
        }, 3000);
      }
    });
  });

  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };
  const observerCallback = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  };
  const observer = new IntersectionObserver(observerCallback, observerOptions);
  const elementsToObserve = document.querySelectorAll('.content-section');
  elementsToObserve.forEach(el => observer.observe(el));
});
</script>

<style>
/* Styles below remain the same as your previous working version */
.vision-phrase {
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  padding: 2px 4px;
  border-radius: 4px;
}
.vision-phrase:hover {
  background-color: #ccfbf1; /* Tailwind teal-100 */
  color: #0f766e; /* Tailwind teal-700 */
}
.section-highlight {
  border-left: 4px solid #0d9488; /* Tailwind teal-600 */
  padding-left: 1rem;
  transition: border-color 0.3s ease;
}
.chart-container {
  position: relative;
  width: 100%;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  height: 300px;
  max-height: 350px;
}
@media (min-width: 768px) {
  .chart-container {
    height: 350px;
    max-height: 400px;
  }
}
.content-section {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}
.content-section.visible {
  opacity: 1;
  transform: translateY(0);
}
</style>