if dot_product > 0:  # Only resolve the collision if they are moving towards each other
                # Elastic collision response using mass and velocity components
                m1 = obj1.mass
                m2 = obj2.mass

                # Ratios for new velocities this works in optimizing the code and allowing for less computational "stress"
                ratio_1 = (m1 - m2) / (m1 + m2)
                ratio_2 = 2 * m2 / (m1 + m2)
                ratio_3 = (m2 - m1) / (m1 + m2)
                ratio_4 = 2 * m1 / (m1 + m2)
                
                # Calculate the new velocities for both objects in the x direction
                v1_new_vx = ratio_1 * obj1.vx + ratio_2 * obj2.vx
                v2_new_vx = ratio_3 * obj2.vx + ratio_4 * obj1.vx
                            
                # Updating the velocties
                obj1.vx = v1_new_vx
                obj2.vx = v2_new_vx

                #increasing the collision count
                self.collision_count += 1
                #sound
                collision_sound.set_volume(0.2)
                collision_sound.play() 
