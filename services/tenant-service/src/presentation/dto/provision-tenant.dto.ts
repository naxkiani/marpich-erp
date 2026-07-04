import {
  IsString,
  IsOptional,
  IsIn,
  IsArray,
  MinLength,
  MaxLength,
  Matches,
} from "class-validator";

export class ProvisionTenantDto {
  @IsString()
  @MinLength(2)
  @MaxLength(128)
  name!: string;

  @IsString()
  @MinLength(2)
  @MaxLength(63)
  @Matches(/^[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$/, {
    message: "slug must be lowercase alphanumeric with hyphens",
  })
  slug!: string;

  @IsString()
  industryPack!: string;

  @IsOptional()
  @IsIn(["starter", "professional", "enterprise"])
  tier?: "starter" | "professional" | "enterprise";

  @IsOptional()
  @IsArray()
  @IsString({ each: true })
  optionalModules?: string[];
}
