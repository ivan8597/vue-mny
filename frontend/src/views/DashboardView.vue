<template>
  <div class="dashboard">
    <h1>Дашборд</h1>
    
    <DateRangeFilter v-model:dateRange="dateRange" />
    
    <TransactionCharts 
      :transactions="filteredTransactions"
      :previousTransactions="[]"
      :categories="categories"
    />

    <TransactionList 
      :transactions="filteredTransactions"
      :categories="categories"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { Dayjs } from 'dayjs';
import dayjs from '@/plugins/dayjs';
import DateRangeFilter from '@/components/DateRangeFilter.vue';
import TransactionCharts from '@/components/TransactionCharts.vue';
import TransactionList from '@/components/TransactionList.vue';
import { useTransactionsStore } from '@/stores/transactions';
import { useCategoriesStore } from '@/stores/categories';

const transactionsStore = useTransactionsStore();
const categoriesStore = useCategoriesStore();

const dateRange = ref<[Dayjs, Dayjs]>([dayjs().subtract(30, 'day'), dayjs()]);

const filteredTransactions = computed(() => {
  if (!dateRange.value || !dateRange.value[0] || !dateRange.value[1]) {
    return transactionsStore.transactions;
  }
  
  return transactionsStore.transactions.filter(t => {
    const date = dayjs(t.date);
    return date.isAfter(dateRange.value[0]) && date.isBefore(dateRange.value[1]);
  });
});

const categories = computed(() => categoriesStore.categories);
</script>

<style scoped lang="scss">
.dashboard {
  min-height: 100vh;
}
</style> 