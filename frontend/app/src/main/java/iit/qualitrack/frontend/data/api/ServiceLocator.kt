package iit.qualitrack.frontend.data.api

import iit.qualitrack.frontend.util.Constants
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import iit.qualitrack.frontend.data.repository.GarmentRepository

object ServiceLocator {
    private val logging = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val authInterceptor = AuthInterceptor()

    private val client =
        OkHttpClient.Builder().addInterceptor(authInterceptor).addInterceptor(logging).build()

    private val retrofit = Retrofit.Builder().baseUrl(Constants.BASE_URL).client(client)
        .addConverterFactory(GsonConverterFactory.create()).build()

    val apiService: ApiService by lazy {
        retrofit.create(ApiService::class.java)
    }

    val repository: GarmentRepository by lazy {
        GarmentRepository(apiService)
    }
}