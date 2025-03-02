<template>
  <MainLayout>
    <div class="categories-container">
      <h1>Категории</h1>
      <n-layout>
        <n-layout-header bordered>
          <n-menu mode="horizontal" :options="menuOptions" />
        </n-layout-header>
        <n-layout-content content-style="padding: 24px;">
          <n-card title="Категории">
            <template #header-extra>
              <n-button @click="showCategoryModal = true">
                Добавить категорию
              </n-button>
            </template>
            <n-grid :cols="2" :x-gap="24">
              <n-grid-item>
                <h3>Доходы</h3>
                <n-list>
                  <n-list-item v-for="category in incomeCategories" :key="category.id">
                    {{ category.name }}
                  </n-list-item>
                </n-list>
              </n-grid-item>
              <n-grid-item>
                <h3>Расходы</h3>
                <n-list>
                  <n-list-item v-for="category in expenseCategories" :key="category.id">
                    {{ category.name }}
                  </n-list-item>
                </n-list>
              </n-grid-item>
            </n-grid>
          </n-card>
        </n-layout-content>
      </n-layout>

      <n-modal v-model:show="showCategoryModal">
        <n-card title="Новая категория" style="width: 600px">
          <category-form @submit="handleCategorySubmit" />
        </n-card>
      </n-modal>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
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
  NMenu,
  NList,
  NListItem
} from 'naive-ui'
import { useAuthStore } from '@/stores/auth'
import { useCategoriesStore } from '@/stores/categories'
import CategoryForm from '@/components/CategoryForm.vue'
import type { Category } from '@/stores/categories'
import MainLayout from '@/layouts/MainLayout.vue'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const categoriesStore = useCategoriesStore()

const showCategoryModal = ref(false)

const menuOptions = [
  {
    label: 'Дашборд',
    key: 'dashboard',
    onClick: () => router.push('/')
  },
  {
    label: 'Категории',
    key: 'categories',
    onClick: () => router.push('/categories')
  },
  {
    label: 'Выйти',
    key: 'logout',
    onClick: () => authStore.logout()
  }
]

const incomeCategories = computed(() => 
  categoriesStore.categories.filter((c: Category) => c.type === 'income')
)

const expenseCategories = computed(() => 
  categoriesStore.categories.filter((c: Category) => c.type === 'expense')
)

const handleCategorySubmit = async (data: any) => {
  try {
    await categoriesStore.createCategory(data)
    showCategoryModal.value = false
    message.success('Категория создана')
  } catch (error) {
    message.error('Ошибка при создании категории')
  }
}

onMounted(async () => {
  await categoriesStore.fetchCategories()
})
</script>

<style scoped>
.categories {
  min-height: 100vh;
}
</style> 