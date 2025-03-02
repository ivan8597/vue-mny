<template>
  <MainLayout>
    <div class="dashboard">
      <h1>Дашборд</h1>
      
      <DateRangeFilter v-model:dateRange="dateRange" />
      
      <n-space class="summary-cards" justify="space-around">
        <n-card title="Доходы">
          <div class="summary-amount income">{{ formatCurrency(summary.income) }}</div>
        </n-card>
        <n-card title="Расходы">
          <div class="summary-amount expense">{{ formatCurrency(summary.expense) }}</div>
        </n-card>
        <n-card title="Баланс">
          <div class="summary-amount" :class="summary.balance >= 0 ? 'income' : 'expense'">
            {{ formatCurrency(summary.balance) }}
          </div>
        </n-card>
      </n-space>
      
      <TransactionCharts 
        :transactions="filteredTransactions"
        :previousTransactions="[]"
        :categories="categories"
      />

      <n-card title="Прогнозирование расходов" class="forecast-card">
        <TransactionForecast :transactions="filteredTransactions" />
      </n-card>

      <div class="actions">
        <n-button type="primary" @click="showTransactionModal = true">
          Добавить транзакцию
        </n-button>
      </div>

      <TransactionList 
        :transactions="filteredTransactions"
        :categories="categories"
      />
      
      <n-modal
        v-model:show="showTransactionModal"
        preset="card"
        title="Новая транзакция"
        style="width: 600px"
      >
        <TransactionForm :showTransactionModal="{ value: showTransactionModal }" />
      </n-modal>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import type { Dayjs } from 'dayjs';
import dayjs from '@/plugins/dayjs';
import DateRangeFilter from '@/components/DateRangeFilter.vue';
import TransactionCharts from '@/components/TransactionCharts.vue';
import TransactionList from '@/components/TransactionList.vue';
import TransactionForm from '@/components/TransactionForm.vue';
import TransactionForecast from '@/components/TransactionForecast.vue';
import MainLayout from '@/layouts/MainLayout.vue';
import { useTransactionsStore } from '@/stores/transactions';
import { useCategoriesStore } from '@/stores/categories';

const transactionsStore = useTransactionsStore();
const categoriesStore = useCategoriesStore();
const showTransactionModal = ref(false);

const dateRange = ref<[Dayjs, Dayjs]>([dayjs().subtract(30, 'day'), dayjs()]);

onMounted(async () => {
  await Promise.all([
    transactionsStore.fetchTransactions(),
    transactionsStore.fetchSummary(),
    categoriesStore.fetchCategories()
  ]);
});

// Следим за изменениями dateRange и перегружаем данные
watch(dateRange, async () => {
  if (dateRange.value && Array.isArray(dateRange.value) && 
      dateRange.value[0]?.isValid() && dateRange.value[1]?.isValid()) {
    const startDate = dateRange.value[0].format('YYYY-MM-DD');
    const endDate = dateRange.value[1].format('YYYY-MM-DD');
    console.log('Date range changed:', { startDate, endDate })
    await Promise.all([
      transactionsStore.fetchTransactions({ startDate, endDate }),
      transactionsStore.fetchSummary({ startDate, endDate })
    ]);
    console.log('Data fetched, filtered transactions:', filteredTransactions.value.length)
  }
}, { deep: true });

const filteredTransactions = computed(() => {
  if (!dateRange.value || !dateRange.value[0] || !dateRange.value[1]) {
    return transactionsStore.transactions;
  }
  
  return transactionsStore.transactions.filter(t => {
    try {
      if (!t.date) return false;
      const date = dayjs(t.date);
      if (!date.isValid()) return false;
      return (!date.isBefore(dateRange.value[0].startOf('day'))) && 
             (!date.isAfter(dateRange.value[1].endOf('day')));
    } catch (error) {
      console.error('Error filtering date:', t.date, error);
      return false;
    }
  });
});

const summary = computed(() => transactionsStore.summary);
const categories = computed(() => categoriesStore.categories);

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0
  }).format(amount);
};
</script>

<style scoped lang="scss">
.dashboard {
  min-height: 100vh;
}

.summary-cards {
  margin-bottom: 24px;
}

.summary-amount {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}

.income {
  color: #18a058;
}

.expense {
  color: #d03050;
}

.actions {
  margin: 24px 0;
  display: flex;
  justify-content: flex-end;
}

.forecast-card {
  margin-top: 24px;
  margin-bottom: 24px;
}

.wide-content {
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
}

.dashboard-content {
  padding: 20px;
  margin: 0 auto;
}
</style> 