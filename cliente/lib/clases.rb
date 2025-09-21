Clases = true # vago

puts "!!!!!!!!!!!!!!!!!!  clases.rb RECARGADO"

# Somos parte del cliente.
# No importa si cada clase es completamente editable, dado que
# la vista no te deja cambiar lo que no se permite.
# (y en produccion, aunque pudieras, el servidor no lo aceptaria xd)

ROLE_NADIE = 0
ROLE_PRESIDENTE = 1
ROLE_VOCAL = 2
ROLE_COORDINADOR = 3
ROLE_VOLUNTARIO = 4

$rolelut = [
    "xxx",
    "Presidente",
    "Vocal",
    "Coordinador",
    "Voluntario",
]

# !!! nos tomamos unas libertades con el cliente !!!
# 
# asumimos 1 unico usuario que usa el view
# el cual usa el cliente
# el cual guarda de forma global y estatica su sesion con el servidor
# 
# no es seguro, pero...
class LocalSession
    
    @@user = nil
    
    def user=(u)
        @@user = u
    end
    def user
        @@user
    end
    def forget_user!
        @@user = nil  
    end
    
    def logged_in?
        return !!@@user
    end
    
    def can_mod_users?
        return !!@@user && @@user.rol == ROLE_PRESIDENTE
    end
    def can_mod_inventory?
        return !!@@user && @@user.rol <= ROLE_VOCAL
    end
    def can_mod_events?
        return !!@@user && (@@user.rol == ROLE_PRESIDENTE || @@user.rol == ROLE_COORDINADOR)
    end
    def can_join_events?
        return !!@@user && @@user.rol <= ROLE_VOLUNTARIO
    end
end

$session = LocalSession.new

class Usuario
    attr_accessor :idusuario, :nombre, :apellido, :nombreUsuario,
        :telefono, :clave, :email, :rol, :activo
    
    def initialize(gRPCobj = nil)
        # se espera que gRPCobj sea una respesta de gRPC
        
        @idusuario = gRPCobj&.idusuario
        @nombreUsuario = gRPCobj&.nombreUsuario
        @nombre = gRPCobj&.nombre
        @apellido = gRPCobj&.apellido
        @telefono = gRPCobj&.telefono
        @clave = gRPCobj&.clave # no tendriamos por que recibir esto
        @email = gRPCobj&.email
        @rol = gRPCobj&.rol #!!!
        @activo = gRPCobj&.activo
    end
    
    def scramble! # para probar
        instance_variables.each do |var|
            vname = var.to_s.delete("@") + rand(100000).to_s
            instance_variable_set(var, vname)
        end
        return self
    end
    
end

class Rol
    attr_accessor :id, :nombre
    
    def initialize(id, nom)
        @id = id
        @nombre = nom
    end
end

class Inventario
    
end

class Evento
    
end
