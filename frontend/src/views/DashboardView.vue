<template>
  <div class="dashboard">
    <n-layout>
      <n-layout-header bordered>
        <n-menu mode="horizontal" :options="menuOptions" />
      </n-layout-header>
      <n-layout-content content-style="padding: 24px;">
        <n-grid :cols="24" :x-gap="24">
          <n-grid-item :span="16">
            <n-card title="Последние транзакции">
              <template #header-extra>
                <n-button @click="showTransactionModal = true">
                  Добавить транзакцию
                </n-button>
              </template>
              <transaction-list :transactions="transactionsStore.transactions" />
            </n-card>
          </n-grid-item>
          <n-grid-item :span="8">
            <n-card title="Сводка">
              <transaction-summary :summary="transactionsStore.summary" />
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-layout-content>
    </n-layout>

    <n-modal v-model:show="showTransactionModal">
      <n-card title="Новая транзакция" style="width: 600px">
        <transaction-form 
          :showTransactionModal="{ value: showTransactionModal }"
          @submit="handleTransactionSubmit" 
        />
      </n-card>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
// import { useRouter } from 'vue-router'
import { 
  useMessage,
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NGrid,
  NGridItem,
  NCard,
  NButton,
  NModal,
  NMenu
} from 'naive-ui/es'
import { useAuthStore } from '@/stores/auth'
import { useTransactionsStore } from '@/stores/transactions'
import { useCategoriesStore } from '@/stores/categories'
import type { Transaction } from '@/types'
import TransactionList from '@/components/TransactionList.vue'
import TransactionForm from '@/components/TransactionForm.vue'
import TransactionSummary from '@/components/TransactionSummary.vue'

// const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const transactionsStore = useTransactionsStore()
const categoriesStore = useCategoriesStore()

const showTransactionModal = ref(false)

const menuOptions = [
  {
    label: 'Дашборд',
    key: 'dashboard'
  },
  {
    label: 'Категории',
    key: 'categories'
  },
  {
    label: 'Выйти',
    key: 'logout',
    onClick: () => authStore.logout()
  }
]

const handleTransactionSubmit = async (data: any) => {
  try {
    await transactionsStore.createTransaction(data)
    showTransactionModal.value = false
    message.success('Транзакция создана')
  } catch (error) {
    message.error('Ошибка при создании транзакции')
  }
}

onMounted(async () => {
  await Promise.all([
    categoriesStore.fetchCategories(),
    transactionsStore.fetchTransactions(),
    transactionsStore.fetchSummary()
  ])
})
</script>

<style scoped lang="scss">
.dashboard {
  min-height: 100vh;
}
</style> 