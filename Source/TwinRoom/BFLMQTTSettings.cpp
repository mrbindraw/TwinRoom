// Copyright 2026 Andrew Bindraw. All Rights Reserved.


#include "BFLMQTTSettings.h"

FMQTTURL UBFLMQTTSettings::GetMQTTURL()
{
	return GetDefault<UMQTTClientSettings>()->DefaultURL;
}

void UBFLMQTTSettings::SetMQTTURL(const FMQTTURL& InUrl)
{
	GetMutableDefault<UMQTTClientSettings>()->DefaultURL = InUrl;
}


int32 UBFLMQTTSettings::GetPublishRate()
{
	return GetDefault<UMQTTClientSettings>()->PublishRate;
}

void UBFLMQTTSettings::SetPublishRate(int32 PublishRate)
{
	GetMutableDefault<UMQTTClientSettings>()->PublishRate = PublishRate;
}


bool UBFLMQTTSettings::IsTLSVerifyServerCertificate()
{
	return GetDefault<UMQTTClientSettings>()->bTlsVerifyServerCertificate;
}

void UBFLMQTTSettings::SetIsTLSVerifyServerCertificate(bool bIsVerify)
{
	GetMutableDefault<UMQTTClientSettings>()->bTlsVerifyServerCertificate = bIsVerify;
}


FString UBFLMQTTSettings::GetTLSCertificateAuthorityFile()
{
	return GetDefault<UMQTTClientSettings>()->TlsCertificateAuthorityFile;
}

void UBFLMQTTSettings::SetTLSCertificateAuthorityFile(const FString& FullPathToCAFile)
{
	GetMutableDefault<UMQTTClientSettings>()->TlsCertificateAuthorityFile = FullPathToCAFile;
}


void UBFLMQTTSettings::SaveMQTTSettings()
{
	const FString IniPath = FConfigCacheIni::GetDestIniFilename(*UMQTTClientSettings::StaticClass()->GetConfigName(), ANSI_TO_TCHAR(FPlatformProperties::PlatformName()), *FPaths::GeneratedConfigDir());
	UE_LOG(LogTemp, Log, TEXT("IniPath: %s"), *IniPath);
	GetMutableDefault<UMQTTClientSettings>()->SaveConfig(CPF_Config, *IniPath);
}
