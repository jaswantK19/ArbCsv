import LoginForm from './components/LoginForm'
import RegistrationForm from './components/RegistrationForm'
import MainDashboard from './components/MainDashboard'
import UploadsList from './components/UploadsList'

export default [
    {
        path:"/login",
        component: LoginForm,
    },
    {
        path: "/",
        component: RegistrationForm
    },
    {
        path:'/register',
        component: RegistrationForm
    },
    {
        path: "/dashboard",
        component: MainDashboard 
    },
    {
        path: "/Sdashboard",
        component: MainDashboard 
    },
    {
        path: '/uploads',
        component: UploadsList
    }

]