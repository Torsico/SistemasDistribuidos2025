Clases = true # vago

puts "Guat!!!"

class Usuario
    attr_accessor :nombre, :apellido, :nombreusuario,
        :telefono, :email, :rol, :activo
    
    def initialize
        @nombre = "[sin nombre]"
        @apellido = "[sin apellido]"
        @nombreusuario = "[sin nombre de usuario]" # unico
        @telefono = "[sin telefono]"
        @clave = "" # no tendriamos por que recibir esto
        @email = "" # unico
        @rol = 0 #!!!
        @activo = false
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
    @@dd
    
    def initialize(id, nom)
        @id = id
        @nombre = nom
    end
end

class Inventario
    
end

class Evento
    
end
