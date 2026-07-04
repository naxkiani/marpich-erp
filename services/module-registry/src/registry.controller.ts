import { Controller, Get, Param, NotFoundException } from "@nestjs/common";
import {
  listIndustryPacks,
  getIndustryPack,
  resolveModulesForPack,
  PLATFORM_MODULES,
  findPlatformModule,
} from "@marpich/shared-kernel";

@Controller()
export class RegistryController {
  @Get("industry-packs")
  listPacks() {
    return { data: listIndustryPacks() };
  }

  @Get("industry-packs/:packId")
  getPack(@Param("packId") packId: string) {
    const pack = getIndustryPack(packId);
    if (!pack) {
      throw new NotFoundException(`Industry pack not found: ${packId}`);
    }
    return {
      data: {
        ...pack,
        allModules: resolveModulesForPack(packId),
      },
    };
  }

  @Get("modules")
  listModules() {
    return { data: PLATFORM_MODULES };
  }

  @Get("modules/:moduleId")
  getModule(@Param("moduleId") moduleId: string) {
    const mod = findPlatformModule(moduleId);
    if (!mod) {
      throw new NotFoundException(`Module not found: ${moduleId}`);
    }
    return { data: mod };
  }

  @Get("industry-packs/:packId/dependency-graph")
  getDependencyGraph(@Param("packId") packId: string) {
    const pack = getIndustryPack(packId);
    if (!pack) {
      throw new NotFoundException(`Industry pack not found: ${packId}`);
    }

    const allModules = resolveModulesForPack(packId);
    const nodes = allModules.map((id) => ({
      id,
      layer: findPlatformModule(id)?.layer ?? "domain",
      required: pack.requiredModules.includes(id),
    }));

    return {
      data: {
        packId,
        nodes,
        requiredCount: pack.requiredModules.length,
        optionalCount: pack.optionalModules.length,
      },
    };
  }
}
