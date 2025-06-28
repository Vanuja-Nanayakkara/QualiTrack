package iit.qualitrack.frontend.data.model

data class SupervisorDashboard(
    val total_inspections: Int,
    val total_flags: Int,
    val inspection_status: Map<String, Int>,
    val flags: Map<String, Int>,
    val team_performance: List<Map<String, Any>>,
    val supervisor: Map<String, Any>,
    val date: String
)
