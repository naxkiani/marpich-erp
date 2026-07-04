import { ApiProperty, ApiPropertyOptional } from "@nestjs/swagger";
import { IsEmail, IsOptional, IsString, IsBoolean, MinLength, MaxLength } from "class-validator";

export class RegisterDto {
  @ApiProperty({ example: "user@hospital.com" })
  @IsEmail()
  email!: string;

  @ApiProperty({ minLength: 12 })
  @IsString()
  @MinLength(12)
  password!: string;

  @ApiProperty({ example: "Dr. Smith" })
  @IsString()
  @MinLength(2)
  @MaxLength(128)
  displayName!: string;

  @ApiPropertyOptional({ example: "en-US" })
  @IsOptional()
  @IsString()
  locale?: string;
}

export class LoginDto {
  @ApiProperty()
  @IsEmail()
  email!: string;

  @ApiProperty()
  @IsString()
  password!: string;

  @ApiPropertyOptional({ description: "TOTP code or backup code" })
  @IsOptional()
  @IsString()
  mfaCode?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  mfaToken?: string;
}

export class SetupMfaDto {
  @ApiProperty({ description: "6-digit TOTP code from authenticator app" })
  @IsString()
  @MinLength(6)
  @MaxLength(8)
  verifyCode!: string;
}

export class CreateRoleDto {
  @ApiProperty({ example: "billing-clerk" })
  @IsString()
  @MinLength(2)
  code!: string;

  @ApiProperty({ example: "Billing Clerk" })
  @IsString()
  name!: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  description?: string;

  @ApiPropertyOptional({ type: [String] })
  @IsOptional()
  @IsString({ each: true })
  permissionCodes?: string[];
}

export class AssignRoleDto {
  @ApiProperty()
  @IsString()
  roleId!: string;
}

export class RefreshTokenDto {
  @ApiProperty()
  @IsString()
  refreshToken!: string;
}

export class LogoutDto {
  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  refreshToken?: string;

  @ApiPropertyOptional({ description: "Revoke all sessions for current user" })
  @IsOptional()
  @IsBoolean()
  revokeAll?: boolean;
}
