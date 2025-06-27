package iit.qualitrack.frontend.data.api

import iit.qualitrack.frontend.data.model.*
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    // Auth
    @POST("register/")
    suspend fun register(@Body req: RegisterRequest): Response<SimpleMessageResponse>

    @POST("login/")
    suspend fun login(@Body req: LoginRequest): Response<LoginResponse>

    @GET("api/user/role/")
    suspend fun getUserRole(): Response<UserRoleResponse>

    @POST("api/user/assign-role/")
    suspend fun assignRole(@Body req: AssignRoleRequest): Response<SimpleRoleResponse>

    // Defects
    @GET("defects/")
    suspend fun listDefects(): Response<PaginatedResponse<Defect>>

    @POST("defects/")
    suspend fun createDefect(@Body req: CreateDefectRequest): Response<Defect>

    // Inspections
    @GET("inspections/")
    suspend fun listInspections(): Response<PaginatedResponse<Inspection>>

    @POST("inspections/")
    suspend fun createInspection(@Body req: CreateInspectionRequest): Response<Inspection>

    // Flags
    @GET("flags/")
    suspend fun listFlags(): Response<PaginatedResponse<Flag>>

    @POST("flags/create/")
    suspend fun createFlag(@Body req: CreateFlagRequest): Response<SimpleMessageResponse>

    // Notifications
    @GET("notifications/")
    suspend fun listNotifications(@Query("supervisor_id") supId: Int): Response<NotificationsResponse>

    @POST("notifications/{id}/read/")
    suspend fun readNotification(@Path("id") id: Int): Response<SimpleMessageResponse>

    @POST("notifications/read-all/")
    suspend fun readAllNotifications(@Body req: ReadAllRequest): Response<SimpleMessageResponse>

    // Dashboards
    @GET("inspectors/dashboard/")
    suspend fun inspectorDashboard(
        @Query("inspector_id") id: Int, @Query("date") date: String
    ): Response<InspectorDashboard>

    @GET("supervisors/dashboard/")
    suspend fun supervisorDashboard(
        @Query("supervisor_id") id: Int, @Query("date") date: String
    ): Response<SupervisorDashboard>

    // **Paginated** supervisors list
    @GET("supervisors/list/")
    suspend fun listSupervisors(): Response<PaginatedResponse<Supervisor>>

    // Analyze an image via Azure Custom Vision and create a FabricDefect
    @Multipart
    @POST("defects/analyze/")
    suspend fun analyzeDefectImage(
        @Part image: MultipartBody.Part
    ): Response<Defect>

    @PATCH("inspections/{id}/")
    suspend fun updateInspectionStatus(
        @Path("id") id: Int, @Body body: RequestBody
    ): Response<Unit>

    @GET
    suspend fun getPaginatedInspectionsByUrl(@Url url: String): Response<PaginatedResponse<Inspection>>

}