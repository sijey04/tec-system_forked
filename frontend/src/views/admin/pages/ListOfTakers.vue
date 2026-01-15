<template>
  <main class="flex-1 overflow-y-auto">
    <!-- Top Navigation -->
    <header class="bg-white shadow-sm sticky top-0 z-40">
      <div class="flex justify-between items-center px-6 py-4">
        <h1 class="text-2xl font-bold text-gray-800">List of Test Takers</h1>
        <div class="flex items-center space-x-4">
          <button @click="exportToCSV" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200">
            <i class="fas fa-file-export mr-2"></i>
            Export CSV
          </button>
          <button @click="printList" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200">
            <i class="fas fa-print mr-2"></i>
            Print
          </button>
        </div>
      </div>
    </header>

    <!-- Content -->
    <div class="p-6">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 font-medium">Total Takers</p>
              <p class="text-3xl font-bold text-gray-800 mt-1">{{ stats.total_takers || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-crimson-100 flex items-center justify-center">
              <i class="fas fa-users text-crimson-600 text-xl"></i>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 font-medium">Programs</p>
              <p class="text-3xl font-bold text-gray-800 mt-1">{{ stats.by_program?.length || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
              <i class="fas fa-book text-blue-600 text-xl"></i>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 font-medium">Test Sessions</p>
              <p class="text-3xl font-bold text-gray-800 mt-1">{{ stats.by_test_session?.length || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center">
              <i class="fas fa-calendar-check text-green-600 text-xl"></i>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 font-medium">Filtered Results</p>
              <p class="text-3xl font-bold text-gray-800 mt-1">{{ filteredTakers.length }}</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
              <i class="fas fa-filter text-purple-600 text-xl"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters Section -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
        <div class="flex flex-wrap gap-4 items-center">
          <div class="relative flex-1 min-w-[200px]">
            <input 
              type="text" 
              v-model="searchQuery"
              placeholder="Search by name, email, school..." 
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-crimson-500 focus:border-transparent"
              @input="debouncedSearch"
            >
            <i class="fas fa-search absolute left-3 top-3 text-gray-400"></i>
          </div>
          
          <select 
            v-model="selectedProgram" 
            class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-crimson-500"
            @change="fetchTakers"
          >
            <option value="">All Programs</option>
            <option v-for="program in programs" :key="program.id" :value="program.id">
              {{ program.name }}
            </option>
          </select>
          
          <select 
            v-model="selectedTestSession" 
            class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-crimson-500"
            @change="fetchTakers"
          >
            <option value="">All Test Sessions</option>
            <option v-for="session in testSessions" :key="session.id" :value="session.id">
              {{ formatDate(session.exam_date) }}
            </option>
          </select>
          
          <button 
            @click="clearFilters" 
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors duration-200"
          >
            <i class="fas fa-times mr-2"></i>
            Clear Filters
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-crimson-600"></div>
      </div>

      <!-- No Data State -->
      <div v-else-if="filteredTakers.length === 0" class="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
        <i class="fas fa-users-slash text-6xl text-gray-300 mb-4"></i>
        <h3 class="text-xl font-semibold text-gray-600 mb-2">No Approved Test Takers Found</h3>
        <p class="text-gray-500">There are no approved appointments matching your criteria.</p>
      </div>

      <!-- Takers Table -->
      <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="p-6 border-b border-gray-100">
          <h2 class="text-xl font-bold text-gray-800">Approved Test Takers</h2>
          <p class="text-sm text-gray-500 mt-1">List of all approved appointments ready for examination</p>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 border-b border-gray-100">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">#</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Full Name</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Email</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Program</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">School</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Test Session</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Test Center</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Room</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Time Slot</th>
                <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="(taker, index) in paginatedTakers" :key="taker.id" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ (currentPage - 1) * itemsPerPage + index + 1 }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-8 h-8 rounded-full bg-crimson-100 flex items-center justify-center mr-3">
                      <i class="fas fa-user text-crimson-600 text-sm"></i>
                    </div>
                    <div>
                      <p class="font-medium text-gray-800">{{ taker.full_name || formatName(taker) }}</p>
                      <p class="text-xs text-gray-500">ID: {{ taker.id }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ taker.email }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">
                    {{ taker.program_name }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 max-w-[200px] truncate" :title="taker.school_name">
                  {{ taker.school_name || 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {{ taker.test_session_exam_date ? formatDate(taker.test_session_exam_date) : 'Not Assigned' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {{ taker.test_center_name || 'Not Assigned' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {{ taker.test_room_name || 'Not Assigned' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {{ taker.assigned_test_time_slot || taker.time_slot || 'Not Assigned' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                  <button 
                    @click="viewDetails(taker.id)" 
                    class="text-crimson-600 hover:text-crimson-800 font-medium"
                    title="View Details"
                  >
                    <i class="fas fa-eye mr-1"></i>
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div class="px-6 py-4 border-t border-gray-100 flex items-center justify-between">
          <div class="text-sm text-gray-500">
            Showing {{ ((currentPage - 1) * itemsPerPage) + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredTakers.length) }} of {{ filteredTakers.length }} entries
          </div>
          <div class="flex space-x-2">
            <button 
              @click="currentPage = 1" 
              :disabled="currentPage === 1"
              class="px-3 py-1 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              <i class="fas fa-angle-double-left"></i>
            </button>
            <button 
              @click="currentPage--" 
              :disabled="currentPage === 1"
              class="px-3 py-1 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              <i class="fas fa-angle-left"></i>
            </button>
            <span class="px-3 py-1 text-gray-700">Page {{ currentPage }} of {{ totalPages }}</span>
            <button 
              @click="currentPage++" 
              :disabled="currentPage === totalPages"
              class="px-3 py-1 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              <i class="fas fa-angle-right"></i>
            </button>
            <button 
              @click="currentPage = totalPages" 
              :disabled="currentPage === totalPages"
              class="px-3 py-1 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              <i class="fas fa-angle-double-right"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Program Breakdown Section -->
      <div v-if="stats.by_program?.length > 0" class="mt-6 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-4">Takers by Program</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div 
            v-for="program in stats.by_program" 
            :key="program.program__id" 
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
            @click="filterByProgram(program.program__id)"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-full bg-crimson-100 flex items-center justify-center mr-3">
                <i class="fas fa-book text-crimson-600"></i>
              </div>
              <span class="font-medium text-gray-700">{{ program.program__name }}</span>
            </div>
            <span class="px-3 py-1 rounded-full text-sm font-bold bg-crimson-600 text-white">
              {{ program.count }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../../api';
import { useToast } from '../../../composables/useToast';

export default {
  name: 'ListOfTakers',
  setup() {
    const router = useRouter();
    const { showToast } = useToast();
    
    const loading = ref(true);
    const takers = ref([]);
    const stats = ref({});
    const programs = ref([]);
    const testSessions = ref([]);
    
    const searchQuery = ref('');
    const selectedProgram = ref('');
    const selectedTestSession = ref('');
    
    const currentPage = ref(1);
    const itemsPerPage = ref(15);
    
    let searchTimeout = null;
    
    // Fetch programs for filter dropdown
    const fetchPrograms = async () => {
      try {
        const response = await api.get('/api/programs/');
        programs.value = response.data;
      } catch (error) {
        console.error('Error fetching programs:', error);
      }
    };
    
    // Fetch test sessions for filter dropdown
    const fetchTestSessions = async () => {
      try {
        const response = await api.get('/api/admin/test-sessions/');
        testSessions.value = response.data;
      } catch (error) {
        console.error('Error fetching test sessions:', error);
      }
    };
    
    // Fetch list of takers
    const fetchTakers = async () => {
      loading.value = true;
      try {
        const params = new URLSearchParams();
        if (selectedProgram.value) params.append('program_id', selectedProgram.value);
        if (selectedTestSession.value) params.append('test_session_id', selectedTestSession.value);
        if (searchQuery.value) params.append('search', searchQuery.value);
        
        const response = await api.get(`/api/admin/list-of-takers/?${params.toString()}`);
        
        if (response.data.success) {
          takers.value = response.data.takers;
          stats.value = response.data.stats;
        } else {
          showToast('Failed to fetch takers', 'error');
        }
      } catch (error) {
        console.error('Error fetching takers:', error);
        showToast('Error fetching list of takers', 'error');
      } finally {
        loading.value = false;
      }
    };
    
    // Debounced search
    const debouncedSearch = () => {
      if (searchTimeout) clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        fetchTakers();
      }, 300);
    };
    
    // Filter by program (from stats cards)
    const filterByProgram = (programId) => {
      selectedProgram.value = programId;
      currentPage.value = 1;
      fetchTakers();
    };
    
    // Clear all filters
    const clearFilters = () => {
      searchQuery.value = '';
      selectedProgram.value = '';
      selectedTestSession.value = '';
      currentPage.value = 1;
      fetchTakers();
    };
    
    // Filtered takers based on local search (for real-time filtering)
    const filteredTakers = computed(() => {
      return takers.value;
    });
    
    // Paginated takers
    const paginatedTakers = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value;
      const end = start + itemsPerPage.value;
      return filteredTakers.value.slice(start, end);
    });
    
    // Total pages
    const totalPages = computed(() => {
      return Math.ceil(filteredTakers.value.length / itemsPerPage.value) || 1;
    });
    
    // Format date
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    };
    
    // Format name from components
    const formatName = (taker) => {
      const parts = [taker.last_name, taker.first_name, taker.middle_name].filter(Boolean);
      return parts.join(', ') || 'N/A';
    };
    
    // View appointment details
    const viewDetails = (id) => {
      router.push(`/admin/appointments/${id}`);
    };
    
    // Export to CSV
    const exportToCSV = () => {
      const headers = ['#', 'Full Name', 'Email', 'Program', 'School', 'Test Session', 'Test Center', 'Room', 'Time Slot'];
      const rows = filteredTakers.value.map((taker, index) => [
        index + 1,
        taker.full_name || formatName(taker),
        taker.email,
        taker.program_name,
        taker.school_name || 'N/A',
        taker.test_session_exam_date ? formatDate(taker.test_session_exam_date) : 'Not Assigned',
        taker.test_center_name || 'Not Assigned',
        taker.test_room_name || 'Not Assigned',
        taker.assigned_test_time_slot || taker.time_slot || 'Not Assigned'
      ]);
      
      const csvContent = [headers, ...rows]
        .map(row => row.map(cell => `"${cell}"`).join(','))
        .join('\n');
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `list_of_takers_${new Date().toISOString().split('T')[0]}.csv`;
      link.click();
      
      showToast('CSV exported successfully', 'success');
    };
    
    // Print list
    const printList = () => {
      window.print();
    };
    
    // Initialize
    onMounted(async () => {
      await Promise.all([
        fetchPrograms(),
        fetchTestSessions(),
        fetchTakers()
      ]);
    });
    
    return {
      loading,
      takers,
      stats,
      programs,
      testSessions,
      searchQuery,
      selectedProgram,
      selectedTestSession,
      currentPage,
      itemsPerPage,
      filteredTakers,
      paginatedTakers,
      totalPages,
      fetchTakers,
      debouncedSearch,
      filterByProgram,
      clearFilters,
      formatDate,
      formatName,
      viewDetails,
      exportToCSV,
      printList
    };
  }
};
</script>

<style scoped>
@media print {
  header, .filters, .pagination, button {
    display: none !important;
  }
  
  .bg-white {
    box-shadow: none !important;
    border: 1px solid #e5e7eb !important;
  }
}
</style>
