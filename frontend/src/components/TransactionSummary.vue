<template>
  <n-space vertical>
    <n-statistic label="Доходы">
      <n-number-animation
        ref="numberAnimationInstRef"
        :from="0"
        :to="summary.income"
        :active="true"
      />
    </n-statistic>
    <n-statistic label="Расходы">
      <n-number-animation
        ref="numberAnimationInstRef"
        :from="0"
        :to="summary.expense"
        :active="true"
      />
    </n-statistic>
    <n-statistic label="Баланс">
      <n-number-animation
        ref="numberAnimationInstRef"
        :from="0"
        :to="summary.balance"
        :active="true"
      />
    </n-statistic>
  </n-space>
</template>

<script setup lang="ts">
defineProps<{
  summary: {
    income: number
    expense: number
    balance: number
  }
}>()
</script> 