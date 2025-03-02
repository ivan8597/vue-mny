<template>
  <div class="savings-goal-list">
    <div class="header-row">
      <h2>Цели накопления</h2>
      <n-button type="primary" @click="showAddModal">
        Добавить цель
      </n-button>
    </div>

    <n-spin :show="isLoading">
      <div v-if="savingsGoals.length === 0 && !isLoading" class="empty-state">
        <n-empty description="У вас пока нет целей накопления" />
      </div>
      
      <div v-else class="goals-grid">
        <n-card 
          v-for="goal in savingsGoals" 
          :key="goal.id"
          class="goal-card"
        >
          <template #header>
            <div class="goal-header">
              <span>{{ goal.name }}</span>
              <n-dropdown :options="actionOptions(goal)" @select="handleAction">
                <n-button quaternary circle>
                  <template #icon>
                    <span>⋮</span>
                  </template>
                </n-button>
              </n-dropdown>
            </div>
          </template>
          
          <div class="goal-content">
            <div class="goal-amounts">
              <div class="current-amount">
                {{ formatCurrency(goal.current_amount) }}
              </div>
              <div class="target-amount">
                из {{ formatCurrency(goal.target_amount) }}
              </div>
            </div>
            
            <n-progress
              :percentage="calculateProgress(goal)"
              :status="getProgressStatus(goal)"
              :show-indicator="false"
            />
            
            <div v-if="goal.deadline" class="goal-deadline">
              Срок: {{ formatDate(goal.deadline) }}
            </div>
          </div>
        </n-card>
      </div>
    </n-spin>

    <n-modal
      v-model:show="modalVisible"
      :title="selectedGoal ? 'Редактировать цель' : 'Добавить цель'"
      @close="closeModal"
    >
      <SavingsGoalForm
        :savings-goal="selectedGoal"
        @submit="handleFormSubmit"
        @cancel="closeModal"
      />
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
// import { NIcon } from 'naive-ui'
import { useMessage, useDialog } from 'naive-ui'
import SavingsGoalForm from './SavingsGoalForm.vue'
import { useSavingsGoalsStore } from '@/stores/savings-goals'
import dayjs from '@/plugins/dayjs'
import { storeToRefs } from 'pinia'

interface SavingsGoal {
  id: number
  name: string
  target_amount: number
  current_amount: number
  deadline?: string
  created_at: string
}

const savingsGoalsStore = useSavingsGoalsStore()
const { savingsGoals, isLoading } = storeToRefs(savingsGoalsStore)
const message = useMessage()
const dialog = useDialog()

const modalVisible = ref(false)
const selectedGoal = ref<SavingsGoal | undefined>(undefined)

onMounted(async () => {
  try {
    await savingsGoalsStore.fetchSavingsGoals()
  } catch (error) {
    message.error('Не удалось загрузить цели накопления')
  }
})

const actionOptions = (goal: SavingsGoal) => [
  {
    label: 'Редактировать',
    key: `edit-${goal.id}`,
    icon: () => '✏️'
  },
  {
    label: 'Удалить',
    key: `delete-${goal.id}`,
    icon: () => '🗑️'
  }
]

const handleAction = (key: string) => {
  const [action, idStr] = key.split('-')
  const id = parseInt(idStr)
  const goal = savingsGoals.value.find((g: SavingsGoal) => g.id === id)
  
  if (!goal) return
  
  if (action === 'edit') {
    showEditModal(goal)
  } else if (action === 'delete') {
    showDeleteConfirm(goal)
  }
}

const showAddModal = () => {
  selectedGoal.value = undefined
  modalVisible.value = true
}

const showEditModal = (goal: SavingsGoal) => {
  selectedGoal.value = goal
  modalVisible.value = true
}

const closeModal = () => {
  modalVisible.value = false
  selectedGoal.value = undefined
}

const handleFormSubmit = async (data: any) => {
  try {
    if (selectedGoal.value) {
      await savingsGoalsStore.updateSavingsGoal(selectedGoal.value.id, data)
      message.success('Цель успешно обновлена')
    } else {
      await savingsGoalsStore.createSavingsGoal(data)
      message.success('Цель успешно создана')
    }
    closeModal()
  } catch (error) {
    message.error('Произошла ошибка при сохранении цели')
  }
}

const showDeleteConfirm = (goal: SavingsGoal) => {
  dialog.warning({
    title: 'Удаление цели',
    content: `Вы действительно хотите удалить цель "${goal.name}"?`,
    positiveText: 'Да',
    negativeText: 'Нет',
    onPositiveClick: async () => {
      try {
        await savingsGoalsStore.deleteSavingsGoal(goal.id)
        message.success('Цель успешно удалена')
      } catch (error) {
        message.error('Не удалось удалить цель')
      }
    }
  })
}

const calculateProgress = (goal: SavingsGoal) => {
  if (goal.target_amount <= 0) return 0
  return Math.min(100, Math.round((goal.current_amount / goal.target_amount) * 100))
}

const getProgressStatus = (goal: SavingsGoal) => {
  const progress = calculateProgress(goal)
  if (progress >= 100) return 'success'
  return 'info'
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0
  }).format(value)
}

const formatDate = (dateString: string) => {
  return dayjs(dateString).format('DD.MM.YYYY')
}
</script>

<style scoped>
.savings-goal-list {
  margin-bottom: 30px;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.goal-card {
  height: 100%;
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.goal-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.goal-amounts {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.current-amount {
  font-size: 20px;
  font-weight: bold;
}

.target-amount {
  color: rgba(0, 0, 0, 0.45);
}

.goal-deadline {
  margin-top: 8px;
  color: rgba(0, 0, 0, 0.65);
}

.empty-state {
  margin: 40px 0;
  text-align: center;
}
</style> 