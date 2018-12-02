from spade.behaviour import CyclicBehaviour
import asyncio


class ChangeLights(CyclicBehaviour):
    def how_busy_is_road(self, streets):
        return sum([self.agent.crossroad.cars[street] for street in streets])

    def road_occupancy(self):
        return {road: self.how_busy_is_road(streets) for road, streets in self.agent.crossroad.roads.items()}

    async def run(self):
        if len(self.agent.crossroad.roads) > 0:
            road_occupancy = self.road_occupancy()
            max_busy_road = max(road_occupancy, key=road_occupancy.get)
            lights_to_change = self.agent.crossroad.roads[max_busy_road]
            for street in self.agent.crossroad.lights:
                self.agent.crossroad.lights[street] = 1 if street in lights_to_change else 0
        await asyncio.sleep(15)
